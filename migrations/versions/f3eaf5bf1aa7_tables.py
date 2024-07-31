"""tables

Revision ID: f3eaf5bf1aa7
Revises: b09e4c2d099f
Create Date: 2024-07-31 19:29:35.004285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3eaf5bf1aa7'
down_revision = 'b09e4c2d099f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('mechanic_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mechanic_id'], ['mechanics.id'], name=op.f('fk_payments_mechanic_id_mechanics')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_payments_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], name=op.f('fk_commissions_payment_id_payments')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commissions')
    op.drop_table('payments')
    # ### end Alembic commands ###