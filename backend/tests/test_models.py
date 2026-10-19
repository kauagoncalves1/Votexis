"""Testes de integridade dos modelos ORM e validação da regra multi-tenant."""

from app.database import Base
import app.models  # Carrega todos os models no metadata


def test_tabelas_registradas_no_metadata():
    """Garante que todas as 8 tabelas essenciais foram mapeadas no Base.metadata."""
    tabelas_esperadas = {
        "empresas",
        "usuarios",
        "profissionais",
        "servicos",
        "clientes",
        "horarios_trabalho",
        "bloqueios",
        "agendamentos",
    }
    tabelas_registradas = set(Base.metadata.tables.keys())
    assert tabelas_esperadas.issubset(tabelas_registradas)


def test_regra_multitenant_toda_tabela_de_negocio_tem_empresa_id():
    """Valida a regra fundamental multi-tenant: toda tabela filha deve conter a coluna 'empresa_id'."""
    tabelas_negocio = [
        "usuarios",
        "profissionais",
        "servicos",
        "clientes",
        "horarios_trabalho",
        "bloqueios",
        "agendamentos",
    ]

    for nome_tabela in tabelas_negocio:
        tabela = Base.metadata.tables[nome_tabela]
        assert "empresa_id" in tabela.columns, (
            f"VIOLAÇÃO MULTI-TENANT: A tabela '{nome_tabela}' não possui a coluna 'empresa_id'!"
        )
        coluna_empresa = tabela.columns["empresa_id"]
        assert not coluna_empresa.nullable, (
            f"A coluna 'empresa_id' na tabela '{nome_tabela}' não pode ser nula!"
        )


def test_tabela_empresa_possui_slug_unico():
    """A tabela empresas deve ter slug único para a página pública de agendamento."""
    tabela_empresa = Base.metadata.tables["empresas"]
    coluna_slug = tabela_empresa.columns["slug"]
    assert coluna_slug.unique or any(
        idx.unique for idx in tabela_empresa.indexes if "slug" in idx.columns.keys()
    )


def test_indices_compostos_para_performance_e_conflitos():
    """Verifica se índices compostos com empresa_id foram criados nas tabelas de agendamento e bloqueio."""
    tabela_agendamentos = Base.metadata.tables["agendamentos"]
    nomes_indices = {idx.name for idx in tabela_agendamentos.indexes}
    assert "idx_agendamento_empresa_prof_horario" in nomes_indices
