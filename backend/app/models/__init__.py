"""Exporta todos os models SQLAlchemy para que o Base.metadata reconheça todas as tabelas."""

from app.models.empresa import Empresa
from app.models.usuario import Usuario, UsuarioRole
from app.models.profissional import Profissional
from app.models.servico import Servico
from app.models.cliente import Cliente
from app.models.horario_trabalho import HorarioTrabalho
from app.models.bloqueio import Bloqueio
from app.models.agendamento import Agendamento, StatusAgendamento

__all__ = [
    "Empresa",
    "Usuario",
    "UsuarioRole",
    "Profissional",
    "Servico",
    "Cliente",
    "HorarioTrabalho",
    "Bloqueio",
    "Agendamento",
    "StatusAgendamento",
]
