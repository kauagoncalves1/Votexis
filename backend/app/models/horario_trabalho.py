"""Modelo HorarioTrabalho: grade de disponibilidade semanal do profissional."""

from datetime import time
from typing import TYPE_CHECKING
from sqlalchemy import Integer, Time, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.empresa import Empresa
    from app.models.profissional import Profissional


class HorarioTrabalho(Base):
    """Define as janelas de expediente do profissional em cada dia da semana (0=Segunda, 6=Domingo)."""

    __tablename__ = "horarios_trabalho"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    profissional_id: Mapped[int] = mapped_column(
        ForeignKey("profissionais.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    dia_semana: Mapped[int] = mapped_column(Integer, nullable=False)  # 0=Segunda ... 6=Domingo
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fim: Mapped[time] = mapped_column(Time, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relacionamentos
    empresa: Mapped["Empresa"] = relationship(back_populates="horarios_trabalho")
    profissional: Mapped["Profissional"] = relationship(
        back_populates="horarios_trabalho"
    )

    __table_args__ = (
        Index(
            "idx_horario_empresa_prof_dia",
            "empresa_id",
            "profissional_id",
            "dia_semana",
        ),
    )
