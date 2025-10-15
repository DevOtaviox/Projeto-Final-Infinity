# 🦇 Projeto Wayne — API e Painel Web (Projeto Final Infinity School)

O **Projeto Wayne** é uma aplicação completa com **FastAPI** no backend e **HTML/CSS/JavaScript** no frontend, construída para gerenciamento de **equipamentos**, **veículos** e **itens de segurança**.  
Inclui autenticação JWT, controle de permissões e CRUDs completos.

---

## 🚀 Tecnologias Utilizadas

### Backend
- **FastAPI** (framework principal)
- **SQLAlchemy** (ORM)
- **Alembic** (migrações do banco)
- **SQLite** (banco padrão local)
- **JWT (JSON Web Token)** para autenticação
- **Pydantic** para validação

### Frontend
- HTML5 + CSS3 (tema “Batcaverna” 🦇)
- JavaScript puro com `fetch()`
- Integração direta com endpoints FastAPI

---

## 🧠 Funcionalidades

- ✅ Registro e login de usuários (com JWT)
- 🔐 Autenticação persistente e rota `/auth/me`
- 🧾 CRUD completo:
  - Equipamentos (`/equipment`)
  - Equipamentos de segurança (`/equipment-safety`)
  - Veículos (`/vehicles`)
- 🧍‍♂️ Controle de acesso:
  - Usuários comuns podem visualizar
  - Admins podem criar, editar e excluir
- 🖥️ Dashboard interativo (com dados e nome do usuário logado)
- 🎨 Tema escuro inspirado no universo do Batman

---

## ⚙️ Como Rodar o Projeto (do zero)

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/DevOtaviox/Projeto-Final-Infinity.git
cd Projeto-Final-Infinity/backEnd
````

---

### 2️⃣ Criar e ativar o ambiente virtual

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Inicializar o banco de dados e o Alembic

#### ⚡ Configurar do zero:

1. **Criar o arquivo de migração inicial:**

   ```bash
   alembic init alembic
   ```

2. No arquivo `alembic.ini`, confirme se o caminho do banco está correto:

   ```
   sqlalchemy.url = sqlite:///./wayne.db
   ```

3. No arquivo `alembic/env.py`, importe sua `Base` e configure:

   ```python
   from wayne_api.database import DATABASE_URL 
   from wayne_api.models import Base
   config.set_main_option("sqlalchemy.url", DATABASE_URL)
   target_metadata = Base.metadata
   ```

4. **Gerar a primeira versão de migração:**

   ```bash
   alembic revision --autogenerate -m "create initial tables"
   ```

5. **Aplicar a migração ao banco:**

   ```bash
   alembic upgrade head
   ```

💡 Isso cria o banco `database.db` com todas as tabelas do projeto.

---

### 5️⃣ Executar o servidor FastAPI

```bash
uvicorn app:app --reload
```

Servidor rodando em:
👉 `http://127.0.0.1:8000`

Documentação automática disponível em:

* Swagger UI → `/docs`
* ReDoc → `/redoc`

---

### 6️⃣ Rodar o Frontend

1. Vá até a pasta `frontEnd`.

2. Abra o arquivo `index.html` no navegador
   (ou use o plugin **Live Server** no VSCode para rodar em `http://127.0.0.1:5500`).

3. Faça login ou registre-se, e acesse o painel (`dashboard.html`).

---

## 🧾 Endpoints principais

| Método                                         | Endpoint         | Descrição                            |
| :--------------------------------------------- | :--------------- | :----------------------------------- |
| `POST`                                         | `/auth/register` | Registra novo usuário                |
| `POST`                                         | `/auth/login`    | Realiza login e retorna token JWT    |
| `GET`                                          | `/auth/me`       | Retorna dados do usuário autenticado |
| `GET`                                          | `/vehicles`      | Lista veículos                       |
| `POST`                                         | `/vehicles`      | Cria novo veículo                    |
| `PATCH`                                        | `/vehicles/{id}` | Atualiza veículo existente           |
| `DELETE`                                       | `/vehicles/{id}` | Remove veículo                       |
| (idem para `/equipment` e `/equipment-safety`) |                  |                                      |

---

## 🦇 Autor

**Otávio Lucas Marques Barbosa**
- Projeto desenvolvido como parte do curso **Infinity School**.
- 📘 Repositório: [DevOtaviox/Projeto-Final-Infinity](https://github.com/DevOtaviox/Projeto-Final-Infinity)

