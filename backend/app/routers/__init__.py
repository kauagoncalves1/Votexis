"""Exporta os routers da aplicação."""

from app.routers.auth import router as auth_router

__all__ = [
    "auth_router",
]
