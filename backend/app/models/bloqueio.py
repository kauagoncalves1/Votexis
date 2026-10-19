"""Modelo Bloqueio: folgas, férias, feriados ou indisponibilidades pontuais."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.empresa import Empresa
    from app.models.profissional import Profissional


class Bloqueio(Base):
    """Bloqueio de agenda pontual (folga, feriado, almoço prolongado). Se profissional_id for None, bloqueia a empresa inteira."""

    __tablename__ = "bloqueios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    profissional_id: Mapped[int | None] = mapped_column(
        ForeignKey("profissionais.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fim: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    motivo: Mapped[str] = mapped_column(String(200), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relacionamentos
    empresa: Mapped["Empresa"] = relationship(back_populates="bloqueios")
    profissional: Mapped["Profissional | None"] = relationship(
        back_populates="bloqueios"
    )

    __table_args__ = (
        Index(
            "idx_bloqueio_empresa_prof_periodo",
            "empresa_id",
            "profissional_id",
            "inicio",
            "fim",
        ),
    )
