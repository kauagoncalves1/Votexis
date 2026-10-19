# Votexis

Plataforma de agendamento multi-empresa (multi-tenant) para pequenos negócios
— barbearias, salões, clínicas.

> **Projeto pessoal para fins de estudo.**

## Stack

| Camada   | Tecnologia                                      |
| -------- | ------------------------------------------------ |
| Backend  | FastAPI · PostgreSQL · SQLAlchemy 2.x · Alembic  |
| Frontend | Next.js (App Router) · TypeScript · Tailwind CSS |
| Infra    | Redis + Celery (partes finais)                   |

## Estrutura

```
Votexis/
├── backend/           # API FastAPI
│   ├── app/
│   │   ├── main.py        # Ponto de entrada
│   │   ├── config.py      # Configurações (.env)
│   │   ├── database.py    # Engine + sessão SQLAlchemy
│   │   ├── models/        # ORM models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── routers/       # Endpoints
│   │   ├── services/      # Lógica de negócio
│   │   └── repositories/  # Acesso ao banco
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/          # (futuro) Next.js
└── README.md
```

## Como rodar (backend)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

pip install -r requirements.txt

# Copie e preencha o .env
cp .env.example .env

# Suba o servidor
uvicorn app.main:app --reload

# Rode os testes
pytest
```

## Licenças de imagens

| Imagem | Origem | Licença |
| ------ | ------ | ------- |
| *(nenhuma ainda)* | — | — |

---

*Commit para fins de estudo — projeto pessoal de aprendizado.*
