# Recommendation Service

## Descrição

Microsserviço responsável por gerar recomendações de livros para os usuários da biblioteca.

O sistema utiliza duas estratégias de recomendação:

### Recomendações Personalizadas

* Usuários sem histórico recebem recomendações dos livros mais populares da plataforma.
* Usuários com histórico recebem recomendações de livros da(s) categoria(s) mais lidas.
* Caso não existam livros suficientes na categoria favorita, o sistema complementa as recomendações com outros livros ainda não lidos.
* Livros já lidos não são recomendados novamente.
* Livros indisponíveis não são recomendados.

### Tendências Globais

* Retorna os livros mais populares da biblioteca com base na quantidade de empréstimos realizados por todos os usuários.


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
* Gerar ranking de livros mais populares da plataforma.
* Evitar recomendar livros já lidos pelo usuário.
* Evitar recomendar livros indisponíveis.

## Integrações

* Book Service (5002)
* Loan Service (5003)

## Endpoints

### Recomendações Personalizadas

* GET /recommendations/user/<id>

### Tendências Globais

* GET /recommendations/trending

## Exemplos de Uso

### Buscar recomendações para um usuário

```http
GET /recommendations/user/3
```

### Buscar tendências globais

```http
GET /recommendations/trending
```

## Regras de Negócio

### Usuário sem histórico

Recebe os 5 livros mais populares da plataforma que estejam disponíveis para empréstimo.

### Usuário com histórico

Recebe recomendações baseadas nas categorias dos livros já emprestados.

### Fallback

Caso não existam livros suficientes na categoria favorita, o sistema completa a lista com outros livros ainda não lidos pelo usuário.

### Limite

O serviço retorna no máximo 5 recomendações por consulta.
