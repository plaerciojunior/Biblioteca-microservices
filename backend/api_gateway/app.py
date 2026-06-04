from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests

import os

app = Flask(__name__)

CORS(app)
USER_SERVICE = os.environ.get('USER_SERVICE_URL', 'http://localhost:5001')
BOOK_SERVICE = os.environ.get('BOOK_SERVICE_URL', 'http://localhost:5002')
LOAN_SERVICE = os.environ.get('LOAN_SERVICE_URL', 'http://localhost:5003')
ANALYTICS_SERVICE = os.environ.get('ANALYTICS_SERVICE_URL', 'http://localhost:5004')
PAYMENT_SERVICE = os.environ.get('PAYMENT_SERVICE_URL', 'http://localhost:5005')
RECOMMENDATION_SERVICE = os.environ.get('RECOMMENDATION_SERVICE_URL', 'http://localhost:5006')

#Rota Raiz
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API Gateway está rodando! As rotas disponíveis são /users, /books, /loans, /analytics, /payments e recommendations/user/."}), 200

#Rota Analytics
@app.route('/analytics/dashboard', methods=['GET'])
def get_analytics():
    response = requests.get(f'{ANALYTICS_SERVICE}/analytics/dashboard')
    return jsonify(response.json()), response.status_code

#ROTAS USUÁRIO

#Login
@app.route('/users/login', methods=['POST'])
def login_usuario():

    response = requests.post(
        f'{USER_SERVICE}/users/login',
        json=request.json
    )

    return jsonify(response.json()), response.status_code

#Logout
@app.route('/users/logout', methods=['POST'])
def logout_usuario():
    response = requests.post(
        f'{USER_SERVICE}/users/logout'
    )

    return jsonify(response.json()), response.status_code

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


#Download / Visualização de PDF do Livro
@app.route('/books/pdf/<filename>', methods=['GET'])
def get_livro_pdf(filename):
    response = requests.get(f'{BOOK_SERVICE}/books/pdf/{filename}')
    if response.status_code == 200:
        return Response(response.content, mimetype=response.headers.get('content-type', 'application/pdf'))
    return jsonify({"Status": "PDF não encontrado"}), response.status_code

#Upload de PDF
@app.route('/books/<int:id>/pdf', methods=['POST'])
def upload_livro_pdf(id):
    if 'file' not in request.files:
        return jsonify({"Status": "Nenhum arquivo enviado"}), 400
    file = request.files['file']
    files = {'file': (file.filename, file.stream, file.mimetype)}
    response = requests.post(f'{BOOK_SERVICE}/books/{id}/pdf', files=files)
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

#Renovar empréstimo
@app.route('/loans/<int:id>/renew', methods=['PUT'])
def renovar_emprestimo(id):

    response = requests.put(
        f'{LOAN_SERVICE}/loans/{id}/renew'
    )

    return jsonify(response.json()), response.status_code

#Limpar multas do usuário
@app.route('/loans/user/<int:id>/clear_fines', methods=['PUT'])
def limpar_multas_usuario(id):
    response = requests.put(
        f'{LOAN_SERVICE}/loans/user/{id}/clear_fines'
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

#Rota de Pagamentos
@app.route('/payments/pay', methods=['POST'])
def processar_pagamento():
    response = requests.post(f'{PAYMENT_SERVICE}/payments/pay', json=request.json)
    return jsonify(response.json()), response.status_code


#ROTA RECOMENDAÇÃO

#Para o usuário (minhas tendências)
@app.route('/recommendations/user/<int:id>', methods=['GET'])
def get_recommendations(id):

    response = requests.get(f'{RECOMMENDATION_SERVICE}/recommendations/user/{id}')

    return jsonify(response.json()), response.status_code

#Geral (tendências globais)
@app.route('/recommendations/trending', methods=['GET'])
def get_trending():

    response = requests.get(
        f'{RECOMMENDATION_SERVICE}/recommendations/trending'
    )

    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)