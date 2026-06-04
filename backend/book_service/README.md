# Book Service

## Descrição

Microsserviço responsável pelo gerenciamento do catálogo de livros da biblioteca.

## Porta

5002

## Tecnologias

* Python
* Flask
* Pony ORM
* SQLite

## Responsabilidades

* Cadastrar livros
* Atualizar livros
* Remover livros
* Controlar disponibilidade dos livros
* Consultar livros cadastrados

## Funcionalidades

* Cadastro de livros
* Atualização de informações
* Exclusão de livros
* Consulta por ID
* Listagem de livros
* Controle de disponibilidade para empréstimos
* Servir arquivos PDF para leitura online
* Receber upload de novos arquivos PDF

## Endpoints

* POST /books
* GET /books
* GET /books/{id}
* PUT /books/{id}
* DELETE /books/{id}
* GET /books/pdf/{filename}
* POST /books/{id}/pdf

## Execução

```bash
pip install -r requirements.txt
python app.py
```
