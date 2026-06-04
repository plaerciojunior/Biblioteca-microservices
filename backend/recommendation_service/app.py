import os
import requests
from flask import Flask, jsonify
from collections import Counter

app = Flask(__name__)

BOOK_SERVICE = os.environ.get(
    "BOOK_SERVICE_URL",
    "http://localhost:5002"
)

LOAN_SERVICE = os.environ.get(
    "LOAN_SERVICE_URL",
    "http://localhost:5003"
)




#Rota para o minhas tendências/recomendação para o usuário
@app.route('/recommendations/user/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):

    loans_response = requests.get(
        f"{LOAN_SERVICE}/loans/user/{user_id}"
    )

    books_response = requests.get(
        f"{BOOK_SERVICE}/books"
    )

    if loans_response.status_code != 200:
        return jsonify({"Status": "Erro ao consultar histórico de empréstimos"}), 500
    
    if books_response.status_code != 200:
        return jsonify({
            "Status": "Erro ao consultar catálogo de livros"
        }), 500

    loans = loans_response.json()
    books = books_response.json()

    # Usuário sem histórico
    if len(loans) == 0:

        all_loans = requests.get(
            f"{LOAN_SERVICE}/loans"
        ).json()

        contador = Counter()

        for loan in all_loans:
            contador[loan["livro_id"]] += 1

        recomendados = []

        for livro_id, _ in contador.most_common():

            livro = next(
                (b for b in books if b["id"] == livro_id),
                None
            )

            # Apenas livros disponíveis
            if livro and livro["disponivel"]:
                recomendados.append(livro)

            # Limita a 5 recomendações
            if len(recomendados) == 5:
                break

        return jsonify(recomendados),200
    
    # Livros já lidos pelo usuário
    livros_lidos = set()

    # Categorias dos livros já lidos
    categorias = []

    for loan in loans:

        livro_id = loan["livro_id"]

        livros_lidos.add(livro_id)

        livro = next(
            (b for b in books if b["id"] == livro_id),
            None
        )

        if livro:
            categorias.append(livro["categoria"])

    # Conta categorias por frequência
    categorias_ordenadas = Counter(
        categorias
    ).most_common()

    recomendacoes = []

    # Tenta recomendar primeiro pelas categorias mais lidas
    for categoria, _ in categorias_ordenadas:

        for livro in books:

            if (
                livro["categoria"] == categoria
                and livro["id"] not in livros_lidos
                and livro not in recomendacoes
                and livro["disponivel"]
            ):
                recomendacoes.append(livro)

        if len(recomendacoes) >= 5:
            break

    # Fallback:
    # Se não encontrou recomendações suficientes,
    # adiciona outros livros ainda não lidos
    if len(recomendacoes) < 5:

        for livro in books:

            if (
                livro["id"] not in livros_lidos
                and livro not in recomendacoes
                and livro["disponivel"]
            ):
                recomendacoes.append(livro)

            if len(recomendacoes) >= 5:
                break

    return jsonify(recomendacoes[:5]),200


#Rota para tendências globais/livros mais populares
@app.route('/recommendations/trending', methods=['GET'])
def get_trending():

    books_response = requests.get(
        f"{BOOK_SERVICE}/books"
    )

    if books_response.status_code != 200:
        return jsonify({
            "Status": "Erro ao consultar catálogo de livros"
        }), 500

    books = books_response.json()

    all_loans = requests.get(
        f"{LOAN_SERVICE}/loans"
    ).json()

    contador = Counter()

    for loan in all_loans:
        contador[loan["livro_id"]] += 1

    recomendados = []

    for livro_id, _ in contador.most_common():

        livro = next(
            (b for b in books if b["id"] == livro_id),
            None
        )

        if livro: # and livro["disponivel"]
            recomendados.append(livro)

        if len(recomendados) == 5:
            break

    return jsonify(recomendados),200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5006
    )