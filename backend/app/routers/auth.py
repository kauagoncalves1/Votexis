"""Rotas da API para autenticação e gestão de contas."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.auth import (
    CadastroEmpresaRequest,
    LoginRequest,
    TokenResponse,
    UsuarioResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/cadastrar-empresa",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar nova empresa e usuário administrador",
)
def cadastrar_empresa(
    dados: CadastroEmpresaRequest,
    db: Session = Depends(get_db),
):
    """Cria uma nova empresa (tenant) e o seu administrador inicial de forma atômica."""
    service = AuthService(db)
    return service.cadastrar_empresa(dados)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login de usuário e obtenção de token JWT",
)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db),
):
    """Autentica o usuário com email e senha, retornando o JWT com claims de tenant."""
    service = AuthService(db)
    return service.autenticar(dados)


@router.get(
    "/me",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter perfil do usuário atualmente autenticado",
)
def obter_usuario_logado(
    usuario_atual: Usuario = Depends(get_current_user),
):
    """Retorna os dados cadastrais do usuário autenticado e da empresa a qual pertence."""
    return usuario_atual
