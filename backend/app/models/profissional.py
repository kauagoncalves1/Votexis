"""Modelo Profissional: prestador de serviços da empresa."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.empresa import Empresa
    from app.models.agendamento import Agendamento
    from app.models.horario_trabalho import HorarioTrabalho
    from app.models.bloqueio import Bloqueio


class Profissional(Base):
    """Profissional que atende clientes na empresa."""

    __tablename__ = "profissionais"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    especialidade: Mapped[str | None] = mapped_column(String(120), nullable=True)
    ativo: Mapped[bool] = mapped_column(default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relacionamentos
    empresa: Mapped["Empresa"] = relationship(back_populates="profissionais")
    agendamentos: Mapped[List["Agendamento"]] = relationship(
        back_populates="profissional", cascade="all, delete-orphan"
    )
    horarios_trabalho: Mapped[List["HorarioTrabalho"]] = relationship(
        back_populates="profissional", cascade="all, delete-orphan"
    )
    bloqueios: Mapped[List["Bloqueio"]] = relationship(
        back_populates="profissional"
    )
