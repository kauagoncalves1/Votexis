"""Exporta todos os repositórios da aplicação."""

from app.repositories.empresa_repo import EmpresaRepository
from app.repositories.usuario_repo import UsuarioRepository

__all__ = [
    "EmpresaRepository",
    "UsuarioRepository",
]
