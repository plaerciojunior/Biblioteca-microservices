from flask import Flask, jsonify, request
from pony.orm import db_session, select, commit
from bd.models import db, Emprestimo
import requests
from datetime import datetime, timezone

app = Flask(__name__)

#Criar um empréstimo de livro
@app.route('/loans', methods=['POST'])
@db_session
def criar_emprestimo():

    data = request.json

    usuario_id = data['usuario_id']
    livro_id = data['livro_id']
    usuario = requests.get(
        f'http://localhost:5001/{int(usuario_id)}'
    )

    if usuario.status_code != 200:
        return jsonify({
            "msg": "Usuário não encontrado"
        }), 404

    # Verificar livro
    livro = requests.get(
        f'http://localhost:5002/books/{int(livro_id)}'
    )

    if livro.status_code != 200:
        return jsonify({
            "msg": "Livro não encontrado"
        }), 404

    livro_data = livro.json()
    if not livro_data['disponivel']:
        return jsonify({
            "msg": "Livro indisponível"
        }), 400

    # Criar empréstimo
    loan = Emprestimo(
        usuario_id=usuario_id,
        livro_id=livro_id
    )

    # Atualizar disponibilidade do livro
    requests.put(
        f'http://localhost:5002/books/{livro_id}',
        json={"disponivel": False}
    )

    return jsonify({
        "msg": "Empréstimo realizado"
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

    return jsonify(resultado)

#Empréstimo por id específico
@app.route('/loans/<int:id>', methods=['GET'])
@db_session
def buscar_emprestimo(id):

    loan = Emprestimo.get(id=id)

    if not loan:
        return jsonify({
            "msg": "Empréstimo não encontrado"
        }), 404

    return jsonify({
        "id": loan.id,
        "usuario_id": loan.usuario_id,
        "livro_id": loan.livro_id,
        "status": loan.status
    })

#Atualizando status do livro/devolução empréstimo
@app.route('/loans/<int:id>', methods=['PUT'])
@db_session
def devolver_livro(id):

    loan = Emprestimo.get(id=id)

    if not loan:
        return jsonify({
            "msg": "Empréstimo não encontrado"
        }), 404

    if loan.status == 'devolvido':
        return jsonify({
            "msg": "Livro já devolvido"
        }), 400

    loan.status = 'devolvido'

    loan.data_devolucao = datetime.now(timezone.utc)
    commit()

    # tornar livro disponível novamente
    requests.put(
        f'http://localhost:5002/books/{loan.livro_id}',
        json={"disponivel": True}
    )

    return jsonify({
        "msg": "Livro devolvido"
    })

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
                "user_id": loan.usuario_id,
                "book_id": loan.livro_id,
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
                "user_id": loan.usuario_id,
                "book_id": loan.livro_id,
                "data_emprestimo": loan.data_emprestimo,
                "data_devolucao": loan.data_devolucao
            })

    return jsonify(resultado)



if __name__ == '__main__':
    app.run(port=5003)