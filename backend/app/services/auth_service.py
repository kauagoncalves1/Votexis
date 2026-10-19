"""Serviço de autenticação e gerenciamento de contas."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.models.usuario import Usuario, UsuarioRole
from app.repositories.empresa_repo import EmpresaRepository
from app.repositories.usuario_repo import UsuarioRepository
from app.schemas.auth import (
    CadastroEmpresaRequest,
    LoginRequest,
    TokenResponse,
    UsuarioResponse,
)
from app.security import (
    criar_access_token,
    gerar_hash_senha,
    verificar_senha,
)


class AuthService:
    """Lógica de negócio para cadastro de tenants, login e emissão de JWT."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.empresa_repo = EmpresaRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def cadastrar_empresa(self, dados: CadastroEmpresaRequest) -> TokenResponse:
        """Cria atomicamente uma nova Empresa e seu usuário Administrador inicial."""
        # 1. Valida unicidade do slug da empresa
        if self.empresa_repo.buscar_por_slug(dados.slug):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"O link/slug '{dados.slug}' já está em uso por outro estabelecimento.",
            )

        # 2. Valida unicidade do email do usuário
        if self.usuario_repo.buscar_por_email(dados.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"O email '{dados.email}' já está cadastrado no sistema.",
            )

        # 3. Transação atômica para criação
        nova_empresa = Empresa(
            nome=dados.nome_empresa.strip(),
            slug=dados.slug,
            telefone=dados.telefone_empresa,
            ativo=True,
        )
        self.empresa_repo.criar(nova_empresa)

        novo_usuario = Usuario(
            empresa_id=nova_empresa.id,
            nome=dados.nome_usuario.strip(),
            email=dados.email.lower().strip(),
            senha_hash=gerar_hash_senha(dados.senha),
            role=UsuarioRole.ADMIN,
            ativo=True,
        )
        self.usuario_repo.criar(novo_usuario)

        self.db.commit()
        self.db.refresh(nova_empresa)
        self.db.refresh(novo_usuario)

        # 4. Gera JWT com o contexto multi-tenant
        token = criar_access_token(
            dados={
                "sub": str(novo_usuario.id),
                "empresa_id": nova_empresa.id,
                "role": novo_usuario.role.value,
                "email": novo_usuario.email,
            }
        )

        return TokenResponse(
            access_token=token,
            usuario=UsuarioResponse.model_validate(novo_usuario),
        )

    def autenticar(self, dados: LoginRequest) -> TokenResponse:
        """Valida credenciais e gera access token com identificador de tenant."""
        usuario = self.usuario_repo.buscar_por_email(dados.email)

        if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este usuário está desativado.",
            )

        if not usuario.empresa.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="A conta desta empresa está desativada.",
            )

        token = criar_access_token(
            dados={
                "sub": str(usuario.id),
                "empresa_id": usuario.empresa_id,
                "role": usuario.role.value,
                "email": usuario.email,
            }
        )

        return TokenResponse(
            access_token=token,
            usuario=UsuarioResponse.model_validate(usuario),
        )
