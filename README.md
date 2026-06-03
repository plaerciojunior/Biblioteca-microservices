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
docker compose up --build
```

- **Frontend (Blazor):** Estará disponível em `http://localhost:8080`
- **API Gateway (Flask):** Estará disponível em `http://localhost:5000`