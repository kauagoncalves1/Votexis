from unittest.mock import MagicMock, patch


def test_health_retorna_200(client):
    """O endpoint /health deve retornar status 200 e campo 'status'."""
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "banco" in body


def test_health_com_banco_ok(client):
    """Verifica resposta quando o banco responde com sucesso."""
    with patch("app.main.engine.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert body["banco"] == "ok"

