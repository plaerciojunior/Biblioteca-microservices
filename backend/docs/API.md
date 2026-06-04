# API Gateway - Sistema de Gerenciamento de Biblioteca

## URL Base

```text
http://localhost:5000
```

---

# Usuários

## Criar usuário

**POST** `/users`

### Body

```json
{
  "nome": "Paulo",
  "email": "paulo@email.com",
  "senha": "123456",
  "tipo": "usuario"
}
```
**Campo `tipo`:**

| Valor | Descrição |
|---------|---------|
| usuario | Usuário comum do sistema |
| admin | Administrador do sistema |

### Resposta (201)

```json
{
  "Status": "Usuário criado",
  "id": 1,
  "email": "paulo@email.com",
  "tipo": "usuario"
}
```

### Erros

**409 Conflict**

```json
{
  "Status": "Email já cadastrado"
}
```

---

## Listar usuários

**GET** `/users`

### Resposta (200)

```json
[
  {
    "id": 1,
    "nome": "Paulo",
    "email": "paulo@email.com",
    "tipo": "usuario"
  }
]
```

---

## Buscar usuário por ID

**GET** `/users/{id}`

### Exemplo

```http
GET /users/1
```

### Resposta (200)

```json
{
  "id": 1,
  "nome": "Paulo",
  "email": "paulo@email.com",
  "tipo": "usuario"
}
```

### Erro (404)

```json
{
  "Status": "Usuário não encontrado"
}
```

---

## Atualizar usuário

**PUT** `/users/{id}`

### Body

Todos os campos são opcionais.

```json
{
  "nome": "Paulo Oliveira",
  "email": "novo@email.com",
  "senha": "novaSenha",
  "tipo": "admin"
}
```

### Resposta (200)

```json
{
  "Status": "Usuário atualizado",
  "id": 1,
  "nome": "Paulo Oliveira",
  "email": "novo@email.com",
  "tipo": "admin"
}
```

### Erro (404)

```json
{
  "Status": "Usuário não encontrado"
}
```

---

## Remover usuário

**DELETE** `/users/{id}`

### Resposta (200)

```json
{
  "Status": "Usuário deletado com sucesso"
}
```

### Erro (404)

```json
{
  "Status": "Usuário não encontrado"
}
```

---

# Livros

## Criar livro

**POST** `/books`

### Body

```json
{
  "nome": "Dom Casmurro",
  "autor": "Machado de Assis",
  "categoria": "Romance",
  "ano_publicacao": 1899,
  "disponivel": true
}
```

### Campo `disponivel`

| Valor | Descrição |
|---------|---------|
| true | Livro disponível para empréstimo |
| false | Livro indisponível para empréstimo |

### Resposta (201)

```json
{
  "Status": "Livro criado",
  "id": 1,
  "nome": "dom casmurro",
  "autor": "Machado de Assis",
  "categoria": "Romance",
  "ano_publicacao": 1899,
  "disponivel": true
}
```

### Erro (409)

```json
{
  "Status": "Livro já cadastrado"
}
```

---

## Listar livros

**GET** `/books`

### Resposta

```json
[
  {
    "id": 1,
    "nome": "dom casmurro",
    "autor": "Machado de Assis",
    "categoria": "Romance",
    "ano_publicacao": 1899,
    "disponivel": true
  }
]
```

---

## Buscar livro por ID

**GET** `/books/{id}`

### Resposta (200)

```json
{
  "id": 1,
  "nome": "dom casmurro",
  "autor": "Machado de Assis",
  "categoria": "Romance",
  "ano_publicacao": 1899,
  "disponivel": true
}
```

### Erro (404)

```json
{
  "Status": "Livro não encontrado"
}
```

---

## Atualizar livro

**PUT** `/books/{id}`

### Body

Todos os campos são opcionais.

```json
{
  "nome": "Memórias Póstumas",
  "autor": "Machado de Assis",
  "categoria": "Romance",
  "ano_publicacao": 1881,
  "disponivel": true
}
```

## Resposta (200)

```json
{
  "id": 1,
  "nome": "Memórias Póstumas",
  "autor": "Machado de Assis",
  "categoria": "Romance",
  "ano_publicacao": 1881,
  "disponivel": true
}
```

### Erro (404)

```json
{
  "Status": "Livro não encontrado"
}
```

---

## Remover livro

**DELETE** `/books/{id}`

### Resposta (200)

```json
{
  "Status": "Livro deletado com sucesso"
}
```

### Erro (404)

```json
{
  "Status": "Livro não encontrado"
}
```

---

# Empréstimos

## Criar empréstimo

**POST** `/loans`

### Body

```json
{
  "usuario_id": 1,
  "livro_id": 2
}
```

### Resposta (201)

```json
{
  "Status": "Empréstimo realizado"
}
```

### Possíveis erros

#### (404) Usuário não encontrado


```json
{
  "Status": "Usuário não encontrado"
}
```

#### (404) Livro não encontrado

```json
{
  "Status": "Livro não encontrado"
}
```

#### (400) Livro indisponível

```json
{
  "Status": "Livro indisponível"
}
```

---

## Listar empréstimos

**GET** `/loans`

### Resposta

```json
[
  {
    "id": 1,
    "usuario_id": 1,
    "livro_id": 2,
    "status": "ativo"
  }
]
```

### Campo `status`

| Valor | Descrição |
|---------|---------|
| ativo | Empréstimo em andamento |
| devolvido | Livro devolvido |

---

## Buscar empréstimo por ID

**GET** `/loans/{id}`

### Resposta (200)

```json
{
  "id": 1,
  "usuario_id": 1,
  "livro_id": 2,
  "status": "ativo"
}
```

## Erro (404)

```json
{
  "Status": "Empréstimo não encontrado"
}
```

---

## Atualizar empréstimo/devolver livro

**PUT** `/loans/{id}`

### Resposta (200)

```json
{
  "Status": "Livro devolvido"
}
```
### Possíveis erros

### Livro já devolvido (400)

```json
{
  "Status": "Livro já devolvido"
}
```

### Empréstimo não encontrado (404)

```json
{
  "Status": "Empréstimo não encontrado"
}
```

---

## Buscar empréstimos de um usuário

**GET** `/loans/user/{id}`

### Exemplo

```http
GET /loans/user/1
```

### Resposta

```json
[
  {
    "id": 1,
    "user_id": 1,
    "book_id": 2,
    "status": "ativo",
    "data_emprestimo": "2026-06-02T12:00:00",
    "data_devolucao": null
  }
]
```

### Campo `data_devolucao`

| Valor | Descrição |
|---------|---------|
| null | Empréstimo ainda ativo/livro ainda não foi devolvido |
| data/hora  | Data que o livro foi devolvido |

---

## Listar empréstimos ativos

**GET** `/loans/active`

### Resposta

```json
[
  {
    "id": 1,
    "user_id": 1,
    "book_id": 2,
    "data_emprestimo": "2026-06-02T12:00:00",
    "data_devolucao": null
  }
]
```

---

# Recomendações

## Recomendações personalizadas

**GET** `/recommendations/user/{id}`

### Exemplo

```http
GET /recommendations/user/1
```

### Descrição

Retorna até 5 livros recomendados com base no histórico de empréstimos do usuário.

Caso o usuário não possua histórico, o sistema retorna os livros mais populares disponíveis.

### Resposta (200)

```json
[
  {
    "id": 9,
    "nome": "1984",
    "autor": "George Orwell",
    "categoria": "Sci-Fi",
    "disponivel": true
  }
]
```

### Possíveis erros

### Erro ao consultar histórico de empréstimos (500)

```json
{
  "Status": "Erro ao consultar histórico de empréstimos"
}
```

### Erro ao consultar catálogo de livros (500)

```json
{
  "Status": "Erro ao consultar catálogo de livros"
}
```

---

## Tendências globais

**GET** `/recommendations/trending`

### Descrição

Retorna os 5 livros mais populares da biblioteca.

### Resposta (200)

```json
[
  {
    "id": 9,
    "nome": "1984",
    "autor": "George Orwell",
    "categoria": "Sci-Fi",
    "disponivel": true
  }
]
```

### Erro ao consultar catálogo de livros (500)

```json
{
  "Status": "Erro ao consultar catálogo de livros"
}
```

---

# CORS

A API possui CORS habilitado através da biblioteca Flask-CORS.

---

# Arquitetura

Frontend
↓
API Gateway (5000)
├─ User Service (5001)
├─ Book Service (5002)
├─ Loan Service (5003)
├─ Analytics Service (5004)
├─ Payment Service (5005)
└─ Recommendation Service (5006)


# Observações

- Todos os dados são enviados e recebidos em JSON.
- Os IDs são gerados automaticamente pelo sistema.
- Um livro emprestado tem seu campo "disponivel" alterado para false.
- Ao devolver um livro, o campo "disponivel" volta para true.
- Senhas são armazenadas utilizando hash e nunca são retornadas pela API.
