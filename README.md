# Vida em Equilíbrio - Backend

API REST desenvolvida em Django para a plataforma de acompanhamento de saúde mental.

## Sobre o Projeto

API responsável por gerenciar usuários (psicólogos e pacientes), relatos, humor e autenticação para o aplicativo **Vida em Equilíbrio**.

## Como Executar

### Pré-requisitos
- Python 3.10+
- pip

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>

# Entre na pasta
cd VidaEmEquilibrio

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
```

### Configuração

Crie um arquivo `.env` na raiz:

```env
SECRET_KEY= # chave secreta para o django
DB_NAME= # nome do banco de dados
DB_USER= # usuário do banco de dados
DB_PASSWORD= # senha do banco de dados
EMAIL_HOST_USER= # email para envio de emails
EMAIL_HOST_PASSWORD= # senha de aplicação do gmail
```

### Executar

```bash
# Aplique as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver

# API disponível em: http://localhost:8000/api/
```

## Endpoints da API

### Autenticação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/login/` | Login de usuário |
| POST | `/api/registrar-psicologo/` | Cadastro de psicólogo |
| POST | `/api/mudar-senha/` | Alterar senha do usuário |

### Psicólogo
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/meus-pacientes/` | Lista de pacientes do psicólogo |
| POST | `/api/adicionar-paciente/` | Adicionar novo paciente |

### Paciente
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/registrar-paciente/` | Cadastro de paciente |
| PUT | `/api/configurar-perfil/` | Configurar perfil (nome e avatar) |
| POST | `/api/salvar-relato/` | Criar relato com humor |
| GET | `/api/meus-relatos-calendario/` | Dados para calendário |

### Relatórios
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/relatos-paciente/<id>/` | Relatórios de um paciente específico |

## Autenticação

A API utiliza **Token Authentication** via Django REST Framework. 


## Integração Frontend

Configure a URL do backend em `src/services/api.js`:

```javascript
const API_URL = 'http://localhost:8000/api';
```

## Links

- **Repositório Frontend**: [vida-em-equilibrio-front](https://github.com/MatheusBenatti/VidaEmEquilibrio-Front)
- **Vídeo Pitch**: [YouTube](https://youtu.be/OxUri_r4I8I)

---

**Global Solution - FIAP 2026**
