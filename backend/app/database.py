"""Engine, SessionLocal e Base do SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# psycopg 3 usa o dialeto 'postgresql+psycopg' no SQLAlchemy 2.x.
# Convertemos a DATABASE_URL padrão para usar o driver correto.
_db_url = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+psycopg://", 1
)

engine = create_engine(
    _db_url,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 3},
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Classe base para todos os models ORM."""


def get_db():
    """Dependency do FastAPI: abre e fecha a sessão do banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
