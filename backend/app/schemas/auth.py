"""Schemas Pydantic para cadastro, login e tokens JWT."""

import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class CadastroEmpresaRequest(BaseModel):
    """Payload para criar uma nova empresa e seu administrador inicial."""

    nome_empresa: str = Field(..., min_length=2, max_length=120)
    slug: str = Field(
        ...,
        min_length=2,
        max_length=80,
        description="Identificador único para a URL pública (letras minúsculas, números e hífens)",
    )
    telefone_empresa: str | None = Field(default=None, max_length=20)
    nome_usuario: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(..., min_length=6, max_length=100)

    @field_validator("slug")
    @classmethod
    def validar_slug(cls, valor: str) -> str:
        slug_formatado = valor.strip().lower()
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug_formatado):
            raise ValueError(
                "O slug deve conter apenas letras minúsculas, números e hífens (ex: barbearia-do-ze)."
            )
        return slug_formatado


class LoginRequest(BaseModel):
    """Payload de login com email e senha."""

    email: EmailStr
    senha: str = Field(..., min_length=1)


class EmpresaInfoResponse(BaseModel):
    """Dados resumidos da empresa associada."""

    id: int
    nome: str
    slug: str

    model_config = {"from_attributes": True}


class UsuarioResponse(BaseModel):
    """Dados públicos do usuário autenticado."""

    id: int
    nome: str
    email: str
    role: str
    empresa_id: int
    empresa: EmpresaInfoResponse | None = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Resposta de autenticação bem-sucedida contendo o JWT."""

    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
