from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app)
USER_SERVICE = 'http://localhost:5001'
BOOK_SERVICE = 'http://localhost:5002'
LOAN_SERVICE = 'http://localhost:5003'
RECOMMENDATION_SERVICE = 'http://localhost:5004'

#ROTAS USUÁRIO

#Criar usuário
@app.route('/users', methods=['POST'])
def criar_usuario():

    response = requests.post(
        f'{USER_SERVICE}/users',
        json=request.json
    )

    return jsonify(response.json()), response.status_code

#Todos os usuários
@app.route('/users', methods=['GET'])
def listar_usuarios():

    response = requests.get(
        f'{USER_SERVICE}/users'
    )

    return jsonify(response.json()), response.status_code

#Usuários por ID
@app.route('/users/<int:id>', methods=['GET'])
def get_usuario(id):

    response = requests.get(
        f'{USER_SERVICE}/users/{id}'
    )

    return jsonify(response.json()), response.status_code


#Atualizar usuário por ID
@app.route('/users/<int:id>', methods=['PUT'])
def put_usuario(id):

    response = requests.put(
        f'{USER_SERVICE}/users/{id}',json=request.json)

    return jsonify(response.json()), response.status_code

#Apagar usuário
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_usuario(id):

    response = requests.delete(
        f'{USER_SERVICE}/users/{id}')

    return jsonify(response.json()), response.status_code

#ROTAS Livro
#Criar Livro
@app.route('/books', methods=['POST'])
def criar_livro():

    response = requests.post(
        f'{BOOK_SERVICE}/books',
        json=request.json
    )

    return jsonify(response.json()), response.status_code
    
#Todos os livros
@app.route('/books', methods=['GET'])
def listar_livros():

    response = requests.get(
        f'{BOOK_SERVICE}/books'
    )

    return jsonify(response.json()), response.status_code

#Livro por ID
@app.route('/books/<int:id>', methods=['GET'])
def get_livro(id):

    response = requests.get(
        f'{BOOK_SERVICE}/books/{id}'
    )

    return jsonify(response.json()), response.status_code

#Atualizar livro
@app.route('/books/<int:id>', methods=['PUT'])
def put_livro(id):

    response = requests.put(
        f'{BOOK_SERVICE}/books/{id}', json=request.json
    )

    return jsonify(response.json()), response.status_code

#Apagar livro
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_livro(id):

    response = requests.delete(
        f'{BOOK_SERVICE}/books/{id}'
    )

    return jsonify(response.json()), response.status_code


#Rotas Empréstimos
#Criar empréstimo
@app.route('/loans', methods=['POST'])
def criar_emprestimo():

    response = requests.post(
        f'{LOAN_SERVICE}/loans',
        json=request.json
    )

    return jsonify(response.json()), response.status_code

#Todos os empréstimos
@app.route('/loans', methods=['GET'])
def listar_emprestimos():

    response = requests.get(
        f'{LOAN_SERVICE}/loans'
    )

    return jsonify(response.json()), response.status_code

#Empréstimos por id
@app.route('/loans/<int:id>', methods=['GET'])
def get_emprestimos(id):

    response = requests.get(
        f'{LOAN_SERVICE}/loans/{id}'
    )

    return jsonify(response.json()), response.status_code

#Devolver livro/encerrar empréstimo
@app.route('/loans/<int:id>', methods=['PUT'])
def encerrar_emprestimo(id):

    response = requests.put(
        f'{LOAN_SERVICE}/loans/{id}'
    )

    return jsonify(response.json()), response.status_code

#Todos os empréstimos de um pelo id do usuário
@app.route('/loans/user/<int:id>', methods=['GET'])
def get_emprestimos_usuario(id):

    response = requests.get(
        f'{LOAN_SERVICE}/loans/user/{id}'
    )

    return jsonify(response.json()), response.status_code

#Empréstimos ativos
@app.route('/loans/active', methods=['GET'])
def listar_emprestimos_ativos():

    response = requests.get(
        f'{LOAN_SERVICE}/loans/active'
    )

    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(port=5000)