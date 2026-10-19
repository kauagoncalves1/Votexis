"""Dependências injetáveis do FastAPI para autenticação e isolamento multi-tenant."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository
from app.security import decodificar_token

security_scheme = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    """Extrai, valida o JWT do header Authorization e retorna o usuário logado."""
    token = credentials.credentials
    payload = decodificar_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: identificador de usuário ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: formato de identificador incorreto.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario_repo = UsuarioRepository(db)
    usuario = usuario_repo.buscar_por_id(user_id)

    if not usuario or not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.empresa or not usuario.empresa.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="A empresa deste usuário está inativa.",
        )

    return usuario


def get_current_tenant_id(
    usuario: Usuario = Depends(get_current_user),
) -> int:
    """Retorna o empresa_id do usuário autenticado para garantir filtro multi-tenant obrigatório."""
    return usuario.empresa_id
