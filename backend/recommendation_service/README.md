# Recommendation Service

## Descrição
Microsserviço responsável por gerar recomendações de livros para os usuários da biblioteca.

O sistema utiliza uma estratégia simples baseada no histórico de empréstimos do usuário:

- Usuários sem histórico recebem recomendações dos livros mais populares da plataforma.
- Usuários com histórico recebem recomendações de livros da(s) categoria(s) mais lidas.
- Caso não existam livros suficientes na categoria favorita, o sistema complementa as recomendações com outros livros ainda não lidos.

## Porta
5006

## Tecnologias
* Python
* Flask
* Requests

## Responsabilidades
* Consultar o histórico de empréstimos do usuário.
* Consultar o catálogo de livros.
* Identificar categorias de maior interesse.
* Recomendar livros semelhantes aos já emprestados.
* Recomendar livros populares para usuários novos.
* Evitar recomendar livros já lidos pelo usuário.

## Integrações
* Book Service (5002)
* Loan Service (5003)

## Endpoints
* GET /recommendations/user/<id>

## Exemplo de Uso

### Buscar recomendações para um usuário

```http
GET /recommendations/user/3