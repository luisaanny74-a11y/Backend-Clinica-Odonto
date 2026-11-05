# Sistema de Triagem e Anamnese - Clínica Odontológica

API RESTful desenvolvida em Python com **FastAPI** e **SQLAlchemy** para gerenciamento completo de uma clínica odontológica universitária.

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Executar](#como-executar)
- [Documentação da API](#documentação-da-api)
- [Endpoints Principais](#endpoints-principais)
- [Modelos de Dados](#modelos-de-dados)
- [Segurança](#segurança)
- [Contribuição](#contribuição)

---

## Sobre o Projeto

Este sistema foi desenvolvido para gerenciar o fluxo completo de atendimento em uma clínica odontológica universitária, abrangendo:

- Cadastro e prontuário de pacientes
- Fichas de anamnese e triagem
- Odontograma digital
- Agendamento de atendimentos
- Controle de filas de triagem
- Gestão de usuários (professores, alunos, recepcionistas)
- Autenticação e autorização via JWT

---

## Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Python | 3.14+ | Linguagem de programação |
| FastAPI | - | Framework web moderno e rápido |
| SQLAlchemy | - | ORM para interação com banco de dados |
| Pydantic | v2 | Validação de dados com suporte a email-validator |
| PyMySQL | - | Driver para MySQL |

### Segurança e Autenticação
| Tecnologia | Descrição |
|------------|-----------|
| JWT | JSON Web Tokens para autenticação |
| passlib | Hashing de senhas |
| bcrypt | Algoritmo de criptografia |

### Servidor
| Tecnologia | Descrição |
|------------|-----------|
| Uvicorn | Servidor ASGI para execução da aplicação |

---

## Estrutura do Projeto

```text
backend-odonto/
├── alembic/                    # Migrações do banco de dados
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
├── .env                        # Variáveis de ambiente locais
├── .env.example                # Modelo de variáveis de ambiente
├── requirements.txt            # Dependências do projeto
└── README.md
```

---

# Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **MySQL** - [Download MySQL](https://dev.mysql.com/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Gerenciador de pacotes pip** (já incluso no Python)

---

### Instalação e Configuração (Passo a Passo)

**1. Clone o repositório**

```text
- Terminal:
git clone https://github.com/seu-usuario/backend-odonto.git
cd backend-odonto
```
```text
- Crie e ative um ambiente virtual:
python -m venv venv
.\venv\Scripts\Activate.ps1
```
```text
- Instale as dependências
pip install -r requirements.txt
```
---

**2. Configure as variáveis de ambiente**

**Crie um arquivo .env na raiz do projeto com base no .env.example:**
- PROJECT_NAME="Sistema de Triagem Odontológica"
- API_V1_STR="/api/v1"
- SECRET_KEY="sua_chave_secreta_aqui"
- ALGORITHM="HS256"
- ACCESS_TOKEN_EXPIRE_MINUTES=480
- DATABASE_URL="mysql+pymysql://usuario:senha@localhost:3306/clinica_odonto"

**3. Inicie o servidor de desenvolvimento:**
```text
- Terminal:
$env:PYTHONPATH="."; python -m uvicorn app.main:app --reload
```
---

# Documentação da API (Swagger / ReDoc)

Após iniciar a aplicação, você pode acessar a documentação interativa gerada automaticamente pelo FastAPI:

- Swagger UI: http://127.0.0.1:8000/docs

- ReDoc: http://127.0.0.1:8000/redoc

---

# Módulos e Endpoints Principais

- /api/v1/auth: Autenticação e geração de tokens JWT.
- /api/v1/usuarios: Gerenciamento de professores, alunos (dentistas) e recepcionistas.
- /api/v1/pacientes: Cadastro e prontuário completo de pacientes.
- /api/v1/fichas: Registro de anamnese e triagem.
- /api/v1/odontograma: Mapeamento visual das faces dentes e procedimentos.
- /api/v1/atendimentos: Fluxo de agendamentos e filas de triagem.
- GET /api/v1/especialidades: Consulta autenticada do catálogo de especialidades.

No início da aplicação, o backend cria a especialidade Semiologia se ainda não existir e cria prontuários para pacientes legados que ainda não tenham um. Os IDs são gerados pelo banco.

  ---

### Dica de Segurança adicional para o repositório:
Como o arquivo **`.env`** está visível na lateral da tela no seu GitHub, remova-o do controle de versão para não expor senhas:

```powershell
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "fix: remove .env do controle de versao"
git push origin main

### Contas locais de teste

Ative `SEED_TEST_USERS=true` no `.env` do backend para criar e sincronizar contas locais automaticamente. As tabelas devem estar migradas. O seed ajusta somente senha e status ativo das contas de teste listadas, usando hash bcrypt compativel com o login; nao altera perfil nem matricula. Mantenha desativado fora do ambiente local.

| Perfil | E-mail | Senha |
|---|---|---|
| Aluno | `aluno@uninassau.edu.br` | `aluno123` |
| Professor | `professor@uninassau.edu.br` | `professor123` |
| Recepcao | `recepcao@uninassau.edu.br` | `recepcao123` |
| Admin | `admin@uninassau.edu.br` | `admin123` |

O Flutter usa `POST /api/v1/auth/login` e `GET /api/v1/usuarios/me`. Configure `--dart-define=API_BASE_URL=http://localhost:8000` (no Android Emulator, use `http://10.0.2.2:8000`).
