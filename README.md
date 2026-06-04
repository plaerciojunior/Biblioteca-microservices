# Sistema de Gerenciamento de Biblioteca

Projeto desenvolvido utilizando arquitetura de microsserviços.


# Alunos

- Antônio Eduardo
- Luiz Guilherme
- Paulo Laercio


## Estrutura

- api_gateway
- user_service
- book_service
- loan_service

## Documentação

A documentação da API pode ser encontrada em:

docs/API.md


# Biblioteca-microservice

## Como rodar a aplicação

O projeto foi unificado utilizando Docker Compose. Para iniciar todos os serviços (Frontend, Backend e Bancos de Dados) de uma só vez, basta ter o Docker instalado e rodar o seguinte comando na raiz do projeto:

```bash
docker-compose up --build
```

### Inicialização e Dados Pré-estabelecidos
Além de inicializar os microsserviços e o frontend, o Docker Compose foi configurado para **popular automaticamente os bancos de dados (SQLite)** com dados pré-estabelecidos (mockados) durante a inicialização. Isso inclui a criação de usuários padrão (como um `admin` e usuários comuns para testes), uma lista de livros catalogados (incluindo o livro "Dom Casmurro" com suporte a leitura de PDF) e alguns empréstimos já ativos. 

Essa abordagem permite que testes de usuário, regras de negócio e funções administrativas sejam validados imediatamente após subir os contêineres, sem a necessidade de cadastros manuais iniciais.

- **Frontend (Blazor):** Estará disponível em `http://localhost:8080`
- **API Gateway (Flask):** Estará disponível em `http://localhost:5000`