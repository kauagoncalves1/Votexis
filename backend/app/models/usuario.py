"""Modelo Usuario: login de administradores e funcionários."""

import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.empresa import Empresa


class UsuarioRole(str, enum.Enum):
    ADMIN = "admin"
    RECEPCAO = "recepcao"
    PROFISSIONAL = "profissional"


class Usuario(Base):
    """Usuário que acessa o painel de uma empresa."""

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UsuarioRole] = mapped_column(
        Enum(UsuarioRole, name="usuario_role_enum"),
        default=UsuarioRole.ADMIN,
        nullable=False,
    )
    ativo: Mapped[bool] = mapped_column(default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relacionamentos
    empresa: Mapped["Empresa"] = relationship(back_populates="usuarios")
