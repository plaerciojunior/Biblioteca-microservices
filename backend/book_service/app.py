import os
from flask import Flask, jsonify, request, send_from_directory
from pony.orm import db_session, select, commit
from bd.models import db, Livro
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Caminho absoluto para a pasta bd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BD_DIR = os.path.join(BASE_DIR, 'bd')

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
        return jsonify({"Status": "Livro já cadastrado"}),409
    else:
        lv = Livro(nome = nome, autor = autor, categoria = categoria, ano_publicacao = ano_publi, disponivel = disponivel)
        commit()
        return jsonify({"Status": "Livro criado", "id": lv.id, "nome": lv.nome, "autor": lv.autor, "categoria": lv.categoria,
                        "ano_publicacao": lv.ano_publicacao,
                        "disponivel": lv.disponivel}),201


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
            "disponivel": livro.disponivel,
            "pdf_url": getattr(livro, 'pdf_url', '')
        })

    return jsonify(lista_livros),200

# GET LIVRO POR ID
@app.route('/books/<int:id>', methods=['GET'])
@db_session
def get_book(id):

    livro = Livro.get(id=id)

    if not livro:
        return jsonify({
            "Status": "Livro não encontrado"
        }), 404

    return jsonify({
            "id": livro.id,
            "nome": livro.nome,
            "autor": livro.autor,
            "categoria": livro.categoria,
            "ano_publicacao": livro.ano_publicacao,
            "disponivel": livro.disponivel,
            "pdf_url": getattr(livro, 'pdf_url', '')
        }),200


# ROTA PARA SERVIR O ARQUIVO PDF
@app.route('/books/pdf/<filename>', methods=['GET'])
def get_pdf(filename):
    # Serve o arquivo a partir da pasta 'bd' absoluta
    return send_from_directory(BD_DIR, filename)

# ROTA PARA UPLOAD DE PDF
@app.route('/books/<int:id>/pdf', methods=['POST'])
@db_session
def upload_pdf(id):
    livro = Livro.get(id=id)
    if not livro:
        return jsonify({"Status": "Livro não encontrado"}), 404
        
    if 'file' not in request.files:
        return jsonify({"Status": "Nenhum arquivo enviado"}), 400
        
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(f"livro_{id}_{file.filename}")
        file.save(os.path.join(BD_DIR, filename))
        livro.pdf_url = filename
        commit()
        return jsonify({"Status": "PDF atualizado com sucesso", "pdf_url": filename}), 200
        
    return jsonify({"Status": "Arquivo inválido, envie um .pdf"}), 400

# UPDATE BOOK
@app.route('/books/<int:id>', methods=['PUT'])
@db_session
def update_book(id):

    livro = Livro.get(id=id)

    if not livro:
        return jsonify({
            "Status": "Livro não encontrado"
        }),404

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

    if 'pdf_url' in data:
        livro.pdf_url = data['pdf_url']

    commit()

    return jsonify({
            "id": livro.id,
            "nome": livro.nome,
            "autor": livro.autor,
            "categoria": livro.categoria,
            "ano_publicacao": livro.ano_publicacao,
            "disponivel": livro.disponivel,
            "pdf_url": getattr(livro, 'pdf_url', '')
        }),200

# DELETE BOOK
@app.route('/books/<int:id>', methods=['DELETE'])
@db_session
def delete_book(id):

    livro = Livro.get(id=id)

    if not livro:
        return jsonify({
            "Status": "Livro não encontrado"
        }),404

    livro.delete()

    commit()

    return jsonify({
        "Status": "Livro deletado com sucesso"
    }),200


def seed_books():
    from pony.orm import db_session
    with db_session:
        if Livro.select().count() == 0:
            Livro(nome="neuromancer", autor="William Gibson", categoria="Cyberpunk / Sci-Fi", ano_publicacao=1984, disponivel=True, pdf_url="")
            Livro(nome="snow crash", autor="Neal Stephenson", categoria="Sci-Fi", ano_publicacao=1992, disponivel=True, pdf_url="")
            Livro(nome="a mão esquerda da escuridão", autor="Ursula K. Le Guin", categoria="Sci-Fi", ano_publicacao=1969, disponivel=True, pdf_url="")
            Livro(nome="dune", autor="Frank Herbert", categoria="Fantasia / Sci-Fi", ano_publicacao=1965, disponivel=True, pdf_url="")
            Livro(nome="foundation", autor="Isaac Asimov", categoria="Classic Sci-Fi", ano_publicacao=1951, disponivel=True, pdf_url="")
            Livro(nome="dom casmurro", autor="Machado de Assis", categoria="Literatura Brasileira", ano_publicacao=1899, disponivel=True, pdf_url="dom_casmurro.pdf")
            Livro(nome="vidas secas", autor="Graciliano Ramos", categoria="Literatura Brasileira", ano_publicacao=1938, disponivel=True, pdf_url="vidas_secas.pdf")
            Livro(nome="o senhor dos anéis", autor="J.R.R. Tolkien", categoria="Fantasia", ano_publicacao=1954, disponivel=True, pdf_url="")
            Livro(nome="1984", autor="George Orwell", categoria="Sci-Fi", ano_publicacao=1949, disponivel=True, pdf_url="")
            Livro(nome="fahrenheit 451", autor="Ray Bradbury", categoria="Sci-Fi", ano_publicacao=1953, disponivel=True, pdf_url="")
            Livro(nome="o nome do vento", autor="Patrick Rothfuss", categoria="Fantasia", ano_publicacao=2007, disponivel=True, pdf_url="")
            commit()
            print("Livros mockados inseridos com sucesso no SQLite!")

if __name__ == '__main__':
    seed_books()
    app.run(host="0.0.0.0", port=5002)



    
