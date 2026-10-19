"""Modelo Servico: serviços oferecidos pela empresa."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, List
from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.empresa import Empresa
    from app.models.agendamento import Agendamento


class Servico(Base):
    """Serviço oferecido no catálogo da empresa (ex: Corte, Manicure, Consulta)."""

    __tablename__ = "servicos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    duracao_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    ativo: Mapped[bool] = mapped_column(default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relacionamentos
    empresa: Mapped["Empresa"] = relationship(back_populates="servicos")
    agendamentos: Mapped[List["Agendamento"]] = relationship(
        back_populates="servico"
    )
