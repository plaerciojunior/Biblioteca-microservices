import os
from flask import Flask, jsonify, request
from pony.orm import db_session, select, commit
from bd.models import db, Emprestimo
import requests
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

USER_SERVICE = os.environ.get('USER_SERVICE_URL', 'http://localhost:5001')
BOOK_SERVICE = os.environ.get('BOOK_SERVICE_URL', 'http://localhost:5002')

def get_utc_now():
    # Retorna uma data naive (sem fuso) em UTC para o Pony ORM salvar perfeitamente no SQLite
    return datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)

def parse_dt(dt):
    if not dt: return None
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def format_dt(dt):
    parsed = parse_dt(dt)
    return parsed.isoformat() if parsed else None

def get_status(loan):
    if loan.status in ['ativo', 'atrasado'] and loan.data_emprestimo:
        dt_emp = parse_dt(loan.data_emprestimo)
        prazo = dt_emp + timedelta(days=14)
        if datetime.now(timezone.utc) > prazo:
            return 'atrasado'
    return loan.status

#Criar um empréstimo de livro
@app.route('/loans', methods=['POST'])
@db_session
def criar_emprestimo():

    data = request.json

    usuario_id = data['usuario_id']
    livro_id = data['livro_id']
    
    # Verificar se já possui este livro ativo
    emprestimo_ativo = select(e for e in Emprestimo if e.usuario_id == usuario_id and e.livro_id == livro_id and e.status == 'ativo').first()
    if emprestimo_ativo:
        return jsonify({"Status": "Você já possui um empréstimo ativo para este livro"}), 400

    usuario = requests.get(
        f'{USER_SERVICE}/users/{usuario_id}'
    )

    if usuario.status_code != 200:
        return jsonify({
            "Status": "Usuário não encontrado"
        }), 404

    # Verificar se o usuário está bloqueado
    usuario_data = usuario.json()
    if not usuario_data.get('ativo', True):
        return jsonify({
            "Status": "Usuário bloqueado. Não é possível realizar novos empréstimos."
        }), 403

    # Verificar livro
    livro = requests.get(
        f'{BOOK_SERVICE}/books/{int(livro_id)}'
    )

    if livro.status_code != 200:
        return jsonify({
            "Status": "Livro não encontrado"
        }), 404

    livro_data = livro.json()
    if not livro_data['disponivel']:
        return jsonify({
            "Status": "Livro indisponível"
        }), 400

    # Criar empréstimo
    loan = Emprestimo(
        usuario_id=usuario_id,
        livro_id=livro_id,
        status='ativo',
        data_emprestimo=get_utc_now()
    )

    # Atualizar disponibilidade do livro
    requests.put(
        f'{BOOK_SERVICE}/books/{livro_id}',
        json={"disponivel": False}
    )

    return jsonify({
        "Status": "Empréstimo realizado"
    }), 201


#Ter todos os empréstimos
@app.route('/loans', methods=['GET'])
@db_session
def listar_emprestimos():

    loans = Emprestimo.select()

    resultado = []

    for loan in loans:  
        resultado.append({
            "id": loan.id,
            "usuario_id": loan.usuario_id,
            "livro_id": loan.livro_id,
            "status": get_status(loan),
            "data_emprestimo": format_dt(loan.data_emprestimo),
            "data_devolucao": format_dt(loan.data_devolucao)
        })

    return jsonify(resultado),200

#Empréstimo por id específico
@app.route('/loans/<int:id>', methods=['GET'])
@db_session
def buscar_emprestimo(id):

    loan = Emprestimo.get(id=id)

    if not loan:
        return jsonify({
            "Status": "Empréstimo não encontrado"
        }), 404

    return jsonify({
        "id": loan.id,
        "usuario_id": loan.usuario_id,
        "livro_id": loan.livro_id,
        "status": get_status(loan),
        "data_emprestimo": format_dt(loan.data_emprestimo),
        "data_devolucao": format_dt(loan.data_devolucao)
    }),200

#Atualizando status do livro/devolução empréstimo
@app.route('/loans/<int:id>', methods=['PUT'])
@db_session
def devolver_livro(id):

    loan = Emprestimo.get(id=id)

    if not loan:
        return jsonify({
            "Status": "Empréstimo não encontrado"
        }), 404

    if loan.status == 'devolvido':
        return jsonify({
            "Status": "Livro já devolvido"
        }), 400

    # Trava de Multa: Impedir devolução se estiver atrasado
    if loan.data_emprestimo:
        dt_emp = parse_dt(loan.data_emprestimo)
        prazo = dt_emp + timedelta(days=14)
        if datetime.now(timezone.utc) > prazo:
            return jsonify({"Status": "Livro com multa pendente. Realize o pagamento antes de devolver."}), 403

    loan.status = 'devolvido'

    loan.data_devolucao = get_utc_now()
    commit()

    # tornar livro disponível novamente
    requests.put(
        f'{BOOK_SERVICE}/books/{loan.livro_id}',
        json={"disponivel": True}
    )

    return jsonify({
        "Status": "Livro devolvido"
    }),200

#Renovar empréstimo
@app.route('/loans/<int:id>/renew', methods=['PUT'])
@db_session
def renovar_emprestimo(id):

    loan = Emprestimo.get(id=id)

    if not loan:
        return jsonify({"Status": "Empréstimo não encontrado"}), 404

    if get_status(loan) != 'ativo':
        return jsonify({"Status": "Livros com multa pendente ou já devolvidos não podem ser renovados"}), 400

    loan.data_emprestimo = get_utc_now()
    commit()

    return jsonify({"Status": "Empréstimo renovado com sucesso"}), 200

#Limpar multas e estender prazo em 1 dia
@app.route('/loans/user/<int:user_id>/clear_fines', methods=['PUT'])
@db_session
def limpar_multas(user_id):
    loans = select(l for l in Emprestimo if l.usuario_id == user_id)
    for loan in loans:
        if get_status(loan) == 'atrasado':
            # Redefine a data de empréstimo para 13 dias atrás
            # Isso garante que o prazo (14 dias) vença amanhã, dando 1 dia extra para devolver
            loan.data_emprestimo = get_utc_now() - timedelta(days=13)
            loan.status = 'ativo'
    commit()
    return jsonify({"Status": "Multas limpas e prazos estendidos"}), 200

#Lista todos os empréstimos de um usuário pelo id
@app.route('/loans/user/<int:user_id>', methods=['GET'])
@db_session
def listar_emprestimos_usuario(user_id):
    loans = Emprestimo.select()[:]

    resultado = []

    for loan in loans:

        if loan.usuario_id == user_id:

            resultado.append({
                "id": loan.id,
                "usuario_id": loan.usuario_id,
                "livro_id": loan.livro_id,
                "status": get_status(loan),
                "data_emprestimo": format_dt(loan.data_emprestimo),
                "data_devolucao": format_dt(loan.data_devolucao)
            })

    return jsonify(resultado)


#Empréstimos Ativos
@app.route('/loans/active', methods=['GET'])
@db_session
def listar_emprestimos_ativos():

    loans = Emprestimo.select()[:]

    resultado = []

    for loan in loans:

        if loan.status in ['ativo', 'atrasado']:

            resultado.append({
                "id": loan.id,
                "usuario_id": loan.usuario_id,
                "livro_id": loan.livro_id,
                "status": get_status(loan),
                "data_emprestimo": format_dt(loan.data_emprestimo),
                "data_devolucao": format_dt(loan.data_devolucao)
            })

    return jsonify(resultado),200



def seed_loans():
    from pony.orm import db_session
    with db_session:
        if Emprestimo.select().count() == 0:
            hoje = get_utc_now()
            # Empréstimos para Alice (id=3) e Case (id=4)
            Emprestimo(usuario_id=3, livro_id=1, status='ativo', data_emprestimo=hoje - timedelta(days=5))
            Emprestimo(usuario_id=3, livro_id=2, status='ativo', data_emprestimo=hoje - timedelta(days=2))
            Emprestimo(usuario_id=4, livro_id=4, status='atrasado', data_emprestimo=hoje - timedelta(days=25)) # Atrasado 11 dias (R$ 27,50 de multa)
            Emprestimo(usuario_id=5, livro_id=3, status='atrasado', data_emprestimo=hoje - timedelta(days=30)) # Atrasado 16 dias (R$ 40,00 de multa)
            Emprestimo(usuario_id=3, livro_id=6, status='ativo', data_emprestimo=hoje - timedelta(days=1))
            
            # Adicionando Histórico (Devolvidos) para alimentar o Analytics
            Emprestimo(usuario_id=4, livro_id=3, status='devolvido', data_emprestimo=hoje - timedelta(days=40), data_devolucao=hoje - timedelta(days=36))
            Emprestimo(usuario_id=3, livro_id=5, status='devolvido', data_emprestimo=hoje - timedelta(days=50), data_devolucao=hoje - timedelta(days=30))
            
            commit()
            print("Empréstimos mockados inseridos com sucesso no SQLite!")

if __name__ == '__main__':
    seed_loans()
    app.run(host="0.0.0.0", port=5003)