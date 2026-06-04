from flask import Flask, jsonify, request
from pony.orm import db_session, select, commit
from bd.models import db, Usuario
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma_chave_secreta_super_segura'

#ROTA DE LOGIN
@app.route('/users/login', methods=['POST'])
@db_session
def login_user():
    data = request.json
    email = data.get('email', '').strip().lower()
    senha = data.get('senha', '')

    if not email or not senha:
        return jsonify({"Status": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.get(email=email)
    
    if usuario and check_password_hash(usuario.senha, senha):
        token = jwt.encode({
            'id': usuario.id,
            'email': usuario.email,
            'tipo': usuario.tipo,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            "token": token,
            "user": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "tipo": usuario.tipo
            }
        }), 200
    else:
        return jsonify({"Status": "Credenciais inválidas"}), 401

# ROTA DE LOGOUT
@app.route('/users/logout', methods=['POST'])
def logout_user():
    return jsonify({"Status": "Logout realizado com sucesso"}), 200

#ROTA PARA CRIAÇÃO DE USUÁRIO
@app.route('/users', methods=['POST'])
@db_session
def create_user():
    data = request.json
    email = data['email'].strip().lower()
    nome = data['nome']
    senha = data['senha']
    tipo = data['tipo']

    usuario_existente = Usuario.get(email=email)
    if usuario_existente:
        return jsonify({"Status": "Email já cadastrado"}),409
    else:
        senha_hash = generate_password_hash(senha)
        usuario = Usuario(nome = nome, email = email, senha = senha_hash, tipo = tipo)
        commit()
        return jsonify({"Status": "Usuário criado",
                        "id": usuario.id, "email":usuario.email, "tipo": usuario.tipo}),201

# GET TODOS OS USUÁRIOS
@app.route('/users', methods=['GET'])
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

    return jsonify(lista_usuarios),200

# GET USUÁRIO POR ID
@app.route('/users/<int:id>', methods=['GET'])
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
    }),200

#ATUALIZAR DADOS DO USUÁRIO
@app.route('/users/<int:id>', methods=['PUT'])
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
    }),200

#Apagar usuário
@app.route('/users/<int:id>', methods=['DELETE'])
@db_session
def delete_user(id):
    usuario = Usuario.get(id=id)

    if not usuario:
        return jsonify({
            "Status": "Usuário  não encontrado"
        }),404

    usuario.delete()
    commit()

    return jsonify({
            "Status": "Usuário deletado com sucesso"
        }),200

    
def seed_users():
    from pony.orm import db_session
    with db_session:
        if Usuario.select().count() == 0:
            Usuario(nome="admin", email="admin", senha=generate_password_hash("123456"), tipo="admin")
            Usuario(nome="user", email="user", senha=generate_password_hash("123456"), tipo="usuario")
            Usuario(nome="Alice Vance", email="alice@example.com", senha=generate_password_hash("senhaalice"), tipo="usuario")
            Usuario(nome="Case Henry", email="case@example.com", senha=generate_password_hash("senhacase"), tipo="usuario")
            Usuario(nome="Fulano Detal", email="fulano@example.com", senha=generate_password_hash("senhafulano"), tipo="usuario")
            commit()
            print("Usuários mockados inseridos com sucesso no SQLite!")

if __name__ == '__main__':
    seed_users()
    app.run(host="0.0.0.0", port=5001)
