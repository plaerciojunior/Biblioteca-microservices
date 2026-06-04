import os
from flask import Flask, jsonify, request
from pony.orm import db_session, select, commit
from bd.models import db, Emprestimo
import requests
from datetime import datetime, timezone

app = Flask(__name__)

USER_SERVICE = os.environ.get('USER_SERVICE_URL', 'http://localhost:5001')
BOOK_SERVICE = os.environ.get('BOOK_SERVICE_URL', 'http://localhost:5002')

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
        data_emprestimo=datetime.now(timezone.utc)
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
            "status": loan.status
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
        "status": loan.status
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

    loan.status = 'devolvido'

    loan.data_devolucao = datetime.now(timezone.utc)
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

    if loan.status != 'ativo':
        return jsonify({"Status": "Apenas empréstimos ativos podem ser renovados"}), 400

    loan.data_emprestimo = datetime.now(timezone.utc)
    commit()

    return jsonify({"Status": "Empréstimo renovado com sucesso"}), 200

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
                "status": loan.status,
                "data_emprestimo": loan.data_emprestimo,
                "data_devolucao": loan.data_devolucao
            })

    return jsonify(resultado)


#Empréstimos Ativos
@app.route('/loans/active', methods=['GET'])
@db_session
def listar_emprestimos_ativos():

    loans = Emprestimo.select()[:]

    resultado = []

    for loan in loans:

        if loan.status == 'ativo':

            resultado.append({
                "id": loan.id,
                "usuario_id": loan.usuario_id,
                "livro_id": loan.livro_id,
                "data_emprestimo": loan.data_emprestimo,
                "data_devolucao": loan.data_devolucao
            })

    return jsonify(resultado),200



def seed_loans():
    from pony.orm import db_session
    with db_session:
        if Emprestimo.select().count() == 0:
            # Empréstimos para Alice (id=3) e Case (id=4)
            # Alice pegou neuromancer (id=1) e snow crash (id=2)
            # Case pegou dune (id=4)
            Emprestimo(usuario_id=3, livro_id=1, status='ativo')
            Emprestimo(usuario_id=3, livro_id=2, status='ativo')
            Emprestimo(usuario_id=4, livro_id=4, status='ativo')
            Emprestimo(usuario_id=3, livro_id=6, status='ativo')
            commit()
            print("Empréstimos mockados inseridos com sucesso no SQLite!")

if __name__ == '__main__':
    seed_loans()
    app.run(host="0.0.0.0", port=5003)