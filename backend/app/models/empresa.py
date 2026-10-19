"""Modelo Empresa: tenant raiz do sistema."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.profissional import Profissional
    from app.models.servico import Servico
    from app.models.cliente import Cliente
    from app.models.agendamento import Agendamento
    from app.models.horario_trabalho import HorarioTrabalho
    from app.models.bloqueio import Bloqueio


class Empresa(Base):
    """Representa a empresa/estabelecimento (tenant)."""

    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(80), unique=True, index=True, nullable=False
    )
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ativo: Mapped[bool] = mapped_column(default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relacionamentos
    usuarios: Mapped[List["Usuario"]] = relationship(
        back_populates="empresa", cascade="all, delete-orphan"
    )
    profissionais: Mapped[List["Profissional"]] = relationship(
        back_populates="empresa", cascade="all, delete-orphan"
    )
    servicos: Mapped[List["Servico"]] = relationship(
        back_populates="empresa", cascade="all, delete-orphan"
    )
    clientes: Mapped[List["Cliente"]] = relationship(
        back_populates="empresa", cascade="all, delete-orphan"
    )
    agendamentos: Mapped[List["Agendamento"]] = relationship(
        back_populates="empresa", cascade="all, delete-orphan"
    )
    horarios_trabalho: Mapped[List["HorarioTrabalho"]] = relationship(
        back_populates="empresa", cascade="all, delete-orphan"
    )
    bloqueios: Mapped[List["Bloqueio"]] = relationship(
        back_populates="empresa", cascade="all, delete-orphan"
    )
