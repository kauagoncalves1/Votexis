"""cria_tabelas_iniciais

Revision ID: c487c5d2d71f
Revises: 
Create Date: 2026-10-19 13:40:13.583825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c487c5d2d71f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Tabela Empresas (tenant raiz)
    op.create_table(
        'empresas',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('slug', sa.String(length=80), nullable=False),
        sa.Column('telefone', sa.String(length=20), nullable=True),
        sa.Column('ativo', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_empresas_slug'), 'empresas', ['slug'], unique=True)

    # 2. Tabela Usuarios
    usuario_role_enum = postgresql.ENUM('admin', 'recepcao', 'profissional', name='usuario_role_enum')
    usuario_role_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('empresa_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('senha_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'recepcao', 'profissional', name='usuario_role_enum'), nullable=False),
        sa.Column('ativo', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['empresa_id'], ['empresas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_empresa_id'), 'usuarios', ['empresa_id'], unique=False)
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)

    # 3. Tabela Profissionais
    op.create_table(
        'profissionais',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('empresa_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('especialidade', sa.String(length=120), nullable=True),
        sa.Column('ativo', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['empresa_id'], ['empresas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profissionais_empresa_id'), 'profissionais', ['empresa_id'], unique=False)

    # 4. Tabela Servicos
    op.create_table(
        'servicos',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('empresa_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('duracao_minutos', sa.Integer(), nullable=False),
        sa.Column('preco', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('ativo', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['empresa_id'], ['empresas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_servicos_empresa_id'), 'servicos', ['empresa_id'], unique=False)

    # 5. Tabela Clientes
    op.create_table(
        'clientes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('empresa_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('telefone', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['empresa_id'], ['empresas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clientes_empresa_id'), 'clientes', ['empresa_id'], unique=False)
    op.create_index(op.f('ix_clientes_telefone'), 'clientes', ['telefone'], unique=False)

    # 6. Tabela Horarios de Trabalho
    op.create_table(
        'horarios_trabalho',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('empresa_id', sa.Integer(), nullable=False),
        sa.Column('profissional_id', sa.Integer(), nullable=False),
        sa.Column('dia_semana', sa.Integer(), nullable=False),
        sa.Column('hora_inicio', sa.Time(), nullable=False),
        sa.Column('hora_fim', sa.Time(), nullable=False),
        sa.Column('ativo', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.ForeignKeyConstraint(['empresa_id'], ['empresas.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['profissional_id'], ['profissionais.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_horario_empresa_prof_dia', 'horarios_trabalho', ['empresa_id', 'profissional_id', 'dia_semana'], unique=False)
    op.create_index(op.f('ix_horarios_trabalho_empresa_id'), 'horarios_trabalho', ['empresa_id'], unique=False)
    op.create_index(op.f('ix_horarios_trabalho_profissional_id'), 'horarios_trabalho', ['profissional_id'], unique=False)

    # 7. Tabela Bloqueios
    op.create_table(
        'bloqueios',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('empresa_id', sa.Integer(), nullable=False),
        sa.Column('profissional_id', sa.Integer(), nullable=True),
        sa.Column('inicio', sa.DateTime(timezone=True), nullable=False),
        sa.Column('fim', sa.DateTime(timezone=True), nullable=False),
        sa.Column('motivo', sa.String(length=200), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['empresa_id'], ['empresas.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['profissional_id'], ['profissionais.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_bloqueio_empresa_prof_periodo', 'bloqueios', ['empresa_id', 'profissional_id', 'inicio', 'fim'], unique=False)
    op.create_index(op.f('ix_bloqueios_empresa_id'), 'bloqueios', ['empresa_id'], unique=False)
    op.create_index(op.f('ix_bloqueios_profissional_id'), 'bloqueios', ['profissional_id'], unique=False)

    # 8. Tabela Agendamentos
    status_agendamento_enum = postgresql.ENUM('pendente', 'confirmado', 'cancelado', 'concluido', name='status_agendamento_enum')
    status_agendamento_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'agendamentos',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('empresa_id', sa.Integer(), nullable=False),
        sa.Column('profissional_id', sa.Integer(), nullable=False),
        sa.Column('servico_id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('inicio', sa.DateTime(timezone=True), nullable=False),
        sa.Column('fim', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.Enum('pendente', 'confirmado', 'cancelado', 'concluido', name='status_agendamento_enum'), nullable=False),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['empresa_id'], ['empresas.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['profissional_id'], ['profissionais.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['servico_id'], ['servicos.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_agendamento_empresa_prof_horario', 'agendamentos', ['empresa_id', 'profissional_id', 'inicio', 'fim'], unique=False)
    op.create_index('idx_agendamento_cliente', 'agendamentos', ['empresa_id', 'cliente_id'], unique=False)
    op.create_index(op.f('ix_agendamentos_empresa_id'), 'agendamentos', ['empresa_id'], unique=False)
    op.create_index(op.f('ix_agendamentos_profissional_id'), 'agendamentos', ['profissional_id'], unique=False)
    op.create_index(op.f('ix_agendamentos_servico_id'), 'agendamentos', ['servico_id'], unique=False)
    op.create_index(op.f('ix_agendamentos_cliente_id'), 'agendamentos', ['cliente_id'], unique=False)
    op.create_index(op.f('ix_agendamentos_status'), 'agendamentos', ['status'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('agendamentos')
    op.execute('DROP TYPE IF EXISTS status_agendamento_enum')
    op.drop_table('bloqueios')
    op.drop_table('horarios_trabalho')
    op.drop_table('clientes')
    op.drop_table('servicos')
    op.drop_table('profissionais')
    op.drop_table('usuarios')
    op.execute('DROP TYPE IF EXISTS usuario_role_enum')
    op.drop_table('empresas')
