"""Fixtures compartilhadas para os testes."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    """Client HTTP de testes (sem banco real necessário para /health mock)."""
    with TestClient(app) as c:
        yield c
