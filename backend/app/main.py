"""Ponto de entrada da API Votexis."""

from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routers.auth import router as auth_router

app = FastAPI(
    title="Votexis API",
    description="Plataforma de agendamento multi-empresa para pequenos negócios.",
    version="0.1.0",
)

app.include_router(auth_router)


@app.get("/health", tags=["infra"])
def health_check():
    """Verifica se a API e o banco de dados estão acessíveis."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as exc:
        db_status = f"erro: {exc}"

    return {
        "status": "ok",
        "banco": db_status,
    }
