"""Add AdminLogout table

Revision ID: d06d6868d17d
Revises: 42d51091f3d7
Create Date: 2024-08-12 14:47:34.381046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd06d6868d17d'
down_revision = '42d51091f3d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_logout',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('logout_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['admin_id'], ['admins.id'], name=op.f('fk_admin_logout_admin_id_admins')),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.drop_index('ix_token_blocklist_jti')
        batch_op.create_index(batch_op.f('ix_token_blocklist_jti'), ['jti'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_blocklist_jti'))
        batch_op.create_index('ix_token_blocklist_jti', ['jti'], unique=False)

    op.drop_table('admin_logout')
    # ### end Alembic commands ###
