# Sistema de Triagem e Anamnese - Clínica Odontológica (Backend)

API RESTful desenvolvida em Python com **FastAPI** e **SQLAlchemy** para gerenciamento de triagem, prontuários, fichas de anamnese, odontograma e agendamento de atendimentos de uma clínica odontológica universitária.

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3.14+
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Driver do Banco de Dados:** PyMySQL / psycopg2
* **Validação de Dados:** [Pydantic v2](https://docs.pydantic.dev/) (com suporte a `email-validator`)
* **Autenticação:** JWT (JSON Web Tokens) com `passlib` / `bcrypt`
* **Servidor ASGI:** [Uvicorn](https://www.uvicorn.org/)

---

## Estrutura do Projeto

```text
backend-odonto/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/      # Rotas da aplicação (auth, pacientes, fichas, etc.)
│   │   │   └── schemas.py      # Schemas Pydantic para validação de entrada/saída
│   │   └── api_router.py       # Roteador central de APIs
│   ├── core/                   # Configurações globais e segurança (JWT, hash)
│   └── main.py                 # Ponto de entrada da aplicação FastAPI
├── domain/                     # Camada de domínio (Modelos SQLAlchemy e Enums)
│   ├── __init__.py
│   ├── enums.py
│   └── models.py
```

# Como Executar o Projeto Localmente
Pré-requisitos
Python 3.10+ instalado.

Banco de Dados MySQL ou PostgreSQL configurado.

Passo a Passo
Clone o repositório:

Bash
git clone [https://github.com/seu-usuario/backend-odonto.git](https://github.com/seu-usuario/backend-odonto.git)
cd backend-odonto
Crie e ative um ambiente virtual (recomendado):

PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
Instale as dependências:

Bash
pip install -r requirements.txt
Configure as Variáveis de Ambiente:
Crie um arquivo .env na raiz do projeto com base no .env.example:

Ini, TOML
PROJECT_NAME="Sistema de Triagem Odontológica"
API_V1_STR="/api/v1"
SECRET_KEY="sua_chave_secreta_aqui"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=480
DATABASE_URL="mysql+pymysql://usuario:senha@localhost:3306/clinica_odonto"
Inicie o servidor de desenvolvimento:

PowerShell
$env:PYTHONPATH="."; python -m uvicorn app.main:app --reload
Documentação da API (Swagger / ReDoc)
Após iniciar a aplicação, você pode acessar a documentação interativa gerada automaticamente pelo FastAPI:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Módulos e Endpoints Principais
/api/v1/auth: Autenticação e geração de tokens JWT.

/api/v1/usuarios: Gerenciamento de professores, alunos (dentistas) e recepcionistas.

/api/v1/pacientes: Cadastro e prontuário completo de pacientes.

/api/v1/fichas: Registro de anamnese e triagem.

/api/v1/odontograma: Mapeamento visual das faces dentes e procedimentos.

/api/v1/atendimentos: Fluxo de agendamentos e filas de triagem.

---

### Como criar e subir no GitHub:

1. **Crie o arquivo no VS Code:**
   No PowerShell, dentro de `backend-odonto`, execute:
   ```powershell
   New-Item -ItemType File README.md -Force
Cole o conteúdo acima no arquivo criado e salve (Ctrl + S).

Suba as alterações para o GitHub:
PowerShell
git add README.md
git commit -m "docs: adiciona documentacao completa no README"
git push origin main
├── .env.example                # Modelo de variáveis de ambiente
├── requirements.txt            # Dependências do projeto
└── README.md
