from flask import Flask, jsonify, request
from pony.orm import db_session, select, commit
from bd.models import db, Usuario
from werkzeug.security import generate_password_hash

app = Flask(__name__)

#ROTA PARA CRIAÇÃO DE USUÁRIO
@app.route('/', methods=['POST'])
@db_session
def create_user():
    data = request.json
    email = data['email'].strip().lower()
    nome = data['nome']
    senha = data['senha']
    tipo = data['tipo']

    usuario_existente = Usuario.get(email=email)
    if usuario_existente:
        return jsonify({"Status": "Email já cadastrado"})
    else:
        senha_hash = generate_password_hash(senha)
        usuario = Usuario(nome = nome, email = email, senha = senha_hash, tipo = tipo)
        commit()
        return jsonify({"Status": "Usuário criado",
                        "id": usuario.id, "email":usuario.email, "tipo": usuario.tipo})

# GET TODOS OS USUÁRIOS
@app.route('/', methods=['GET'])
@db_session
def get_users():

    usuarios = Usuario.select()

    lista_usuarios = []

    for usuario in usuarios:
        lista_usuarios.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo": usuario.tipo
        })

    return jsonify(lista_usuarios)

# GET USUÁRIO POR ID
@app.route('/<int:id>', methods=['GET'])
@db_session
def get_user(id):

    usuario = Usuario.get(id=id)

    if not usuario:
        return jsonify({
            "Status": "Usuário não encontrado"
        }), 404

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo
    })

#ATUALIZAR DADOS DO USUÁRIO
@app.route('/<int:id>', methods=['PUT'])
@db_session
def update_user(id):

    usuario = Usuario.get(id=id)

    if not usuario:
        return jsonify({
            "Status": "Usuário não encontrado"
        }), 404

    data = request.json

    usuario.nome = data.get('nome', usuario.nome)

    if 'email' in data:
        usuario.email = data['email'].strip().lower()

    if 'tipo' in data:
        usuario.tipo = data['tipo']

    if 'senha' in data:
        usuario.senha = generate_password_hash(data['senha'])

    commit()

    return jsonify({
        "Status": "Usuário atualizado",
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo
    })

    
    
    
if __name__ == "__main__":
    app.run(port=5001, debug=True)

