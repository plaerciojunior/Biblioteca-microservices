# Sistema de Gerenciamento de Biblioteca

Este projeto implementa um Sistema de Gerenciamento de Biblioteca ("Digital Sanctuary") utilizando uma arquitetura de microsserviços com Docker, Python (Flask) e C# (Blazor WebAssembly).


# Alunos

- Antônio Eduardo
- Luiz Guilherme
- Paulo Laercio


## Estrutura

O backend é composto por 6 microsserviços independentes, orquestrados por um API Gateway. O frontend é uma SPA (Single Page Application) moderna e reativa.

- **Backend (Python/Flask)**
  - `api_gateway` (Porta 5000)
  - `user_service` (Porta 5001)
  - `book_service` (Porta 5002)
  - `loan_service` (Porta 5003)
  - `analytics_service` (Porta 5004)
  - `payment_service` (Porta 5005)
- **Frontend (C# / Blazor)**

## Documentação

A documentação da API pode ser encontrada em:

docs/API.md

## Fluxo da Aplicação

### Fluxo do Leitor (Usuário)
1. O leitor realiza cadastro/login.
2. Explora o Catálogo e escolhe um livro disponível.
3. Realiza o Empréstimo com um clique. O livro fica indisponível para outros.
4. Lê os PDFs dos livros onlines diretamente num leitor minimalista e sem distrações.
5. Devolve ou renova o livro pela sua área. Caso atrase, o saldo devedor congela a conta até o pagamento da multa via `payment_service`.

### Fluxo do Staff (Administrador)
1. Acessa uma área restrita e loga com privilégios.
2. Visualiza as estatísticas globais via `analytics_service` no Dashboard, podendo exportar em CSV.
3. Gerencia o Inventário: cadastra novos livros subindo arquivos PDF diretamente.
4. Gerencia Leitores: visualiza status de leitura, revoga empréstimos remotos e pode bloquear contas infratoras.


# Biblioteca-microservice