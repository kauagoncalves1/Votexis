"""Testes de integração para os fluxos de autenticação (cadastro de empresa, login e /me)."""


def test_cadastrar_empresa_com_sucesso(client):
    """Deve cadastrar uma nova empresa e seu administrador, retornando JWT."""
    payload = {
        "nome_empresa": "Barbearia Vintage",
        "slug": "barbearia-vintage",
        "telefone_empresa": "11999998888",
        "nome_usuario": "Carlos Barbeiro",
        "email": "carlos@vintage.com",
        "senha": "senha-segura-123",
    }
    resp = client.post("/auth/cadastrar-empresa", json=payload)
    assert resp.status_code == 201
    dados = resp.json()

    assert "access_token" in dados
    assert dados["token_type"] == "bearer"
    assert dados["usuario"]["email"] == "carlos@vintage.com"
    assert dados["usuario"]["role"] == "admin"
    assert dados["usuario"]["empresa_id"] is not None


def test_rejeitar_cadastro_com_slug_duplicado(client):
    """Não deve permitir criar duas empresas com o mesmo slug/link."""
    payload1 = {
        "nome_empresa": "Barbearia Alpha",
        "slug": "barbearia-alpha",
        "nome_usuario": "Admin Alpha",
        "email": "alpha1@teste.com",
        "senha": "senha-forte-123",
    }
    resp1 = client.post("/auth/cadastrar-empresa", json=payload1)
    assert resp1.status_code == 201

    payload2 = {
        "nome_empresa": "Outra Alpha",
        "slug": "barbearia-alpha",  # Mesmo slug
        "nome_usuario": "Admin Alpha 2",
        "email": "alpha2@teste.com",
        "senha": "senha-forte-123",
    }
    resp2 = client.post("/auth/cadastrar-empresa", json=payload2)
    assert resp2.status_code == 409
    assert "já está em uso" in resp2.json()["detail"]


def test_rejeitar_cadastro_com_email_duplicado(client):
    """Não deve permitir criar usuário com email já existente."""
    payload1 = {
        "nome_empresa": "Studio Beleza",
        "slug": "studio-beleza",
        "nome_usuario": "Ana Cabeleireira",
        "email": "ana@studio.com",
        "senha": "senha-forte-123",
    }
    resp1 = client.post("/auth/cadastrar-empresa", json=payload1)
    assert resp1.status_code == 201

    payload2 = {
        "nome_empresa": "Studio Beleza Filial",
        "slug": "studio-beleza-filial",
        "nome_usuario": "Ana Silva",
        "email": "ana@studio.com",  # Mesmo email
        "senha": "outra-senha-123",
    }
    resp2 = client.post("/auth/cadastrar-empresa", json=payload2)
    assert resp2.status_code == 409
    assert "já está cadastrado" in resp2.json()["detail"]


def test_login_com_sucesso(client):
    """Deve autenticar usuário com credenciais válidas e retornar token."""
    # 1. Cadastra empresa e usuário
    client.post(
        "/auth/cadastrar-empresa",
        json={
            "nome_empresa": "Clínica Saúde",
            "slug": "clinica-saude",
            "nome_usuario": "Dra. Paula",
            "email": "paula@saude.com",
            "senha": "medica-senha-2026",
        },
    )

    # 2. Faz login
    resp = client.post(
        "/auth/login",
        json={
            "email": "paula@saude.com",
            "senha": "medica-senha-2026",
        },
    )
    assert resp.status_code == 200
    dados = resp.json()
    assert "access_token" in dados
    assert dados["usuario"]["email"] == "paula@saude.com"


def test_login_com_senha_incorreta(client):
    """Deve rejeitar login com senha errada com status 401."""
    client.post(
        "/auth/cadastrar-empresa",
        json={
            "nome_empresa": "Barbearia Teste",
            "slug": "barbearia-teste",
            "nome_usuario": "Barbeiro",
            "email": "barbeiro@teste.com",
            "senha": "senha-correta-123",
        },
    )

    resp = client.post(
        "/auth/login",
        json={
            "email": "barbeiro@teste.com",
            "senha": "senha-ERRADA-123",
        },
    )
    assert resp.status_code == 401
    assert "Email ou senha incorretos" in resp.json()["detail"]


def test_login_com_email_inexistente(client):
    """Deve rejeitar login com email não cadastrado com status 401."""
    resp = client.post(
        "/auth/login",
        json={
            "email": "naoexiste@teste.com",
            "senha": "qualquer-senha",
        },
    )
    assert resp.status_code == 401


def test_obter_me_com_token_valido(client):
    """Deve retornar os dados do perfil autenticado usando o Bearer token."""
    cad_resp = client.post(
        "/auth/cadastrar-empresa",
        json={
            "nome_empresa": "Salão VIP",
            "slug": "salao-vip",
            "nome_usuario": "Renata VIP",
            "email": "renata@vip.com",
            "senha": "vip-senha-123",
        },
    )
    token = cad_resp.json()["access_token"]

    resp = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    dados = resp.json()
    assert dados["nome"] == "Renata VIP"
    assert dados["email"] == "renata@vip.com"
    assert dados["role"] == "admin"
    assert dados["empresa"]["slug"] == "salao-vip"


def test_obter_me_sem_token_retorna_401(client):
    """Acesso à rota protegida sem header de autenticação deve ser barrado."""
    resp = client.get("/auth/me")
    assert resp.status_code in (401, 403)
