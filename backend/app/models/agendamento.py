"""Modelo Agendamento: registro de horário marcado."""

import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.empresa import Empresa
    from app.models.profissional import Profissional
    from app.models.servico import Servico
    from app.models.cliente import Cliente


class StatusAgendamento(str, enum.Enum):
    PENDENTE = "pendente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    CONCLUIDO = "concluido"


class Agendamento(Base):
    """Agendamento de serviço com profissional, cliente e horário definidos."""

    __tablename__ = "agendamentos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    profissional_id: Mapped[int] = mapped_column(
        ForeignKey("profissionais.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    servico_id: Mapped[int] = mapped_column(
        ForeignKey("servicos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fim: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[StatusAgendamento] = mapped_column(
        Enum(StatusAgendamento, name="status_agendamento_enum"),
        default=StatusAgendamento.PENDENTE,
        nullable=False,
        index=True,
    )
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
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
    empresa: Mapped["Empresa"] = relationship(back_populates="agendamentos")
    profissional: Mapped["Profissional"] = relationship(back_populates="agendamentos")
    servico: Mapped["Servico"] = relationship(back_populates="agendamentos")
    cliente: Mapped["Cliente"] = relationship(back_populates="agendamentos")

    __table_args__ = (
        Index(
            "idx_agendamento_empresa_prof_horario",
            "empresa_id",
            "profissional_id",
            "inicio",
            "fim",
        ),
        Index("idx_agendamento_cliente", "empresa_id", "cliente_id"),
    )
