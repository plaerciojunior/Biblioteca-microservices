from flask import Flask, jsonify, request
from pony.orm import db_session, select, commit
from bd.models import db, Livro

app = Flask(__name__)

#Rota para criação do livro
@app.route('/books', methods=['POST'])
@db_session
def create_book():
    data = request.json
    nome = data['nome'].strip().lower()
    autor = data['autor']
    categoria = data['categoria']
    ano_publi = data['ano_publicacao']
    disponivel = data['disponivel']
    


    livro = Livro.get(nome = nome)
    if livro:
        return jsonify({"Status": "Livro já cadastrado"})
    else:
        lv = Livro(nome = nome, autor = autor, categoria = categoria, ano_publicacao = ano_publi, disponivel = disponivel)
        commit()
        return jsonify({"Status": "Livro criado", "id": lv.id, "nome": lv.nome, "autor": lv.autor, "categoria": lv.categoria,
                        "ano_publicacao": lv.ano_publicacao,
                        "disponivel": lv.disponivel})


#GET TODOS OS LIVROS
@app.route('/books', methods=['GET'])
@db_session
def get_books():

    livros = Livro.select()

    lista_livros = []

    for livro in livros:
        lista_livros.append({
            "id": livro.id,
            "nome": livro.nome,
            "autor": livro.autor,
            "categoria": livro.categoria,
            "ano_publicacao": livro.ano_publicacao,
            "disponivel": livro.disponivel
        })

    return jsonify(lista_livros)

# GET LIVRO POR ID
@app.route('/books/<int:id>', methods=['GET'])
@db_session
def get_book(id):

    livro = Livro.get(id=id)

    if not livro:
        return jsonify({
            "Status": "Livro não encontrado"
        }), 400

    return jsonify({
            "id": livro.id,
            "nome": livro.nome,
            "autor": livro.autor,
            "categoria": livro.categoria,
            "ano_publicacao": livro.ano_publicacao,
            "disponivel": livro.disponivel
        })

# UPDATE BOOK
@app.route('/books/<int:id>', methods=['PUT'])
@db_session
def update_book(id):

    livro = Livro.get(id=id)

    if not livro:
        return jsonify({
            "Status": "Livro não encontrado"
        })

    data = request.json

    if 'nome' in data:
        livro.nome = data['nome'].strip().lower()

    if 'autor' in data:
        livro.autor = data['autor']

    if 'categoria' in data:
        livro.categoria = data['categoria']

    if 'ano_publicacao' in data:
        livro.ano_publicacao = data['ano_publicacao']

    if 'disponivel' in data:
        livro.disponivel = data['disponivel']

    commit()

    return jsonify({
            "id": livro.id,
            "nome": livro.nome,
            "autor": livro.autor,
            "categoria": livro.categoria,
            "ano_publicacao": livro.ano_publicacao,
            "disponivel": livro.disponivel
        })

# DELETE BOOK
@app.route('/books/<int:id>', methods=['DELETE'])
@db_session
def delete_book(id):

    livro = Livro.get(id=id)

    if not livro:
        return jsonify({
            "message": "Livro não encontrado"
        })

    livro.delete()

    commit()

    return jsonify({
        "message": "Livro deletado com sucesso"
    })


app.run(port=5002)



    
