"""Repositório de acesso a dados para Empresas."""

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.empresa import Empresa


class EmpresaRepository:
    """Operações de banco de dados para a entidade Empresa."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_por_id(self, empresa_id: int) -> Empresa | None:
        return self.db.get(Empresa, empresa_id)

    def buscar_por_slug(self, slug: str) -> Empresa | None:
        query = select(Empresa).where(Empresa.slug == slug)
        return self.db.scalars(query).first()

    def criar(self, empresa: Empresa) -> Empresa:
        self.db.add(empresa)
        self.db.flush()
        return empresa
