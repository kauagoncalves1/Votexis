"""Repositório de acesso a dados para Usuários."""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.models.usuario import Usuario


class UsuarioRepository:
    """Operações de banco de dados para a entidade Usuario."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        query = (
            select(Usuario)
            .options(joinedload(Usuario.empresa))
            .where(Usuario.id == usuario_id)
        )
        return self.db.scalars(query).first()

    def buscar_por_email(self, email: str) -> Usuario | None:
        query = (
            select(Usuario)
            .options(joinedload(Usuario.empresa))
            .where(Usuario.email == email.lower().strip())
        )
        return self.db.scalars(query).first()

    def criar(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.flush()
        return usuario
