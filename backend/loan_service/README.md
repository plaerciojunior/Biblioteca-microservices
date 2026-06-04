# Loan Service

## Descrição

Microsserviço responsável pelo gerenciamento dos empréstimos de livros.

## Porta

5003

## Tecnologias

* Python
* Flask
* Pony ORM
* SQLite
* Requests

## Responsabilidades

* Registrar empréstimos
* Registrar devoluções
* Consultar empréstimos
* Controlar status dos empréstimos
* Integrar User Service e Book Service

## Funcionalidades

* Criação de empréstimos
* Devolução de livros
* Consulta por ID
* Listagem de empréstimos
* Listagem de empréstimos ativos
* Listagem de empréstimos por usuário
* Renovação de empréstimos
* Limpeza de multas após pagamento

## Regras de Negócio

* O usuário deve existir para realizar um empréstimo.
* O livro deve existir para realizar um empréstimo.
* O livro deve estar disponível.
* Ao criar um empréstimo, o livro torna-se indisponível.
* Ao devolver um livro, o status do empréstimo muda para "devolvido".
* Ao devolver um livro, sua disponibilidade volta para true.
* Um usuário bloqueado não pode realizar novos empréstimos.
* Um livro com multa pendente (atrasado) não pode ser devolvido ou renovado.

## Endpoints

* POST /loans
* GET /loans
* GET /loans/{id}
* PUT /loans/{id}
* GET /loans/user/{id}
* GET /loans/active
* PUT /loans/{id}/renew
* PUT /loans/user/{id}/clear_fines

## Dependências

Este serviço depende de:

* User Service (5001)
* Book Service (5002)

## Execução

```bash
pip install -r requirements.txt
python app.py
```
