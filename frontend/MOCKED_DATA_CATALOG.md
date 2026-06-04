# Catálogo de Dados Mockados (Mocked Data Catalog)

Este documento elenca todos os dados estáticos (mockados) utilizados atualmente no frontend da aplicação. O objetivo deste catálogo é servir como base para popular os bancos de dados do backend (SQLite) no momento de criação dos contêineres Docker, permitindo a substituição dos dados estáticos por chamadas reais de API.

## 1. Livros (Books)

Abaixo estão os livros hardcoded encontrados nas páginas (ex: `Home.razor`, `Landing.razor`, `Admin/Dashboard.razor`, `Admin/Inventory.razor`):

| Título (Title) / Nome | Autor (Author) | Categoria (Category/Genres) | ISBN | Status no Mock |
| :--- | :--- | :--- | :--- | :--- |
| **Neuromancer** | William Gibson | Cyberpunk / Sci-Fi | 978-0441569595 | Available |
| **Snow Crash** | Neal Stephenson | Sci-Fi | 978-0553380958 | Loaned |
| **A Mão Esquerda da Escuridão** | Ursula K. Le Guin | - | 978-0441478125 | Available |
| **Dune** | Frank Herbert | Epic Fantasy | 978-0441172719 | Overdue |
| **Foundation** | Isaac Asimov | Classic Sci-Fi | - | - |
| **Mona Lisa Overdrive** | William Gibson | Cyberpunk | - | - |
| **Form & Space** | Francis D.K. | - | - | - |
| **Hackers** | Steven Levy | - | - | - |
| **Grid Systems** | J. Müller-Brockmann | - | - | - |
| **Typography** | Emil Ruder | - | - | - |
| **Simulacra** | Jean Baudrillard | - | - | - |
| **Dom Casmurro** | Machado de Assis | Literatura Brasileira | - | Available (Com PDF) |

*(A maioria desses livros também possui uma `CoverUrl` associada no frontend puxada do Unsplash).*

### Arquivos PDF (Leitura Online)
Para otimizar o projeto e evitar custos de deploy com armazenamento de múltiplos arquivos pesados, a maioria dos livros continuará utilizando a exibição de PDF mockada em `PdfReader.razor`. 
Foi definido que **apenas 1 livro (Dom Casmurro)** terá um arquivo de PDF real (`dom_casmurro.pdf`) vinculado e servido pelo backend para demonstrar a funcionalidade completa de ponta a ponta.
* **Local do arquivo:** `backend/book_service/bd/dom_casmurro.pdf`

## 2. Usuários (Users)

Usuários encontrados mockados no sistema (ex: `Admin/Users.razor` e `Admin/AdminLogin.razor`):

1. **Admin System**
   * **Login/Username:** admin
   * **Senha (Password):** admin
   * **Tipo:** admin

2. **Alice Vance**
   * **Tipo:** usuario
   * **Possui empréstimos:** Sim (Neuromancer, Snow Crash)

3. **Case Henry**
   * **Tipo:** usuario
   * **Possui empréstimos:** Sim (Dune)

## 3. Empréstimos (Loans)

Empréstimos mapeados (ex: `Admin/BookDetail.razor`, `Admin/Users.razor`, `MyLoans.razor`):

| Usuário | Livro | Status de Empréstimo | Observação |
| :--- | :--- | :--- | :--- |
| Alice Vance | Neuromancer | Atrasado (Overdue) | Data de devolução no passado |
| Alice Vance | Snow Crash | Ativo | Data de devolução no futuro |
| Case Henry | Dune | Ativo | - |
| (Usuário Logado) | Simulacra | Devolvido (Returned) | Devolvido há 46 dias |
| (Usuário Logado) | Form & Space | Devolvido (Returned) | Devolvido há 110 dias |

---

## 4. Discrepâncias e Observações (Frontend vs Backend Models)

Ao analisar os modelos de banco de dados (`models.py`) atuais em comparação com o frontend, há algumas diferenças nas propriedades que precisarão ser resolvidas no backend antes de popularmos os dados:

### Modelo Livro (`book_service`)
* **Campos atuais no BD:** `id`, `nome`, `autor`, `categoria`, `ano_publicacao`, `disponivel`, `criado_em`.
* **Faltando no BD (usado no frontend):** `ISBN`, `CoverUrl` (link da imagem de capa).
* O frontend usa `Status` (Available, Loaned, Overdue) em vez de apenas um boolean `disponivel`. Isso pode ser uma derivação baseada nos empréstimos, mas deve ser avaliado.

### Modelo Usuário (`user_service`)
* **Campos atuais no BD:** `id`, `nome`, `email`, `senha`, `tipo`.
* O frontend exibe `AvatarUrl` ou `Initials`, mas isso pode ser gerado dinamicamente ou adicionado ao BD se desejado.

### Modelo Empréstimo (`loan_service`)
* **Campos atuais no BD:** `id`, `usuario_id`, `livro_id`, `data_emprestimo`, `data_devolucao`, `status`.
* O frontend usa `Type` (Physical / Online), então pode ser necessário incluir um campo de `tipo_emprestimo` no modelo de empréstimo.