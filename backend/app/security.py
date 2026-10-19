"""Utilitários de segurança: hash de senha e manipulação de tokens JWT."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from jose import JWTError, jwt
import bcrypt

from app.config import settings


def gerar_hash_senha(senha_plana: str) -> str:
    """Gera o hash bcrypt seguro de uma senha plana."""
    senha_bytes = senha_plana.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha_bytes, salt).decode("utf-8")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Valida se a senha plana bate com o hash armazenado."""
    try:
        senha_bytes = senha_plana.encode("utf-8")[:72]
        hash_bytes = senha_hash.encode("utf-8")
        return bcrypt.checkpw(senha_bytes, hash_bytes)
    except Exception:
        return False


def criar_access_token(dados: Dict[str, Any], expira_em: timedelta | None = None) -> str:
    """Gera um JWT assinado com claims de usuário e tenant."""
    dados_para_codificar = dados.copy()
    if expira_em:
        expiracao = datetime.now(timezone.utc) + expira_em
    else:
        expiracao = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    dados_para_codificar.update({"exp": expiracao})
    token = jwt.encode(
        dados_para_codificar,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return token


def decodificar_token(token: str) -> Dict[str, Any] | None:
    """Decodifica e valida assinatura e expiração do JWT. Retorna None se inválido."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None
