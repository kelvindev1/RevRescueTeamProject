"""adds assistance requests

Revision ID: e15521d7ac30
Revises: f3eaf5bf1aa7
Create Date: 2024-07-31 22:07:03.084520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e15521d7ac30'
down_revision = 'f3eaf5bf1aa7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assistance_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('mechanic_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('resolved', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['mechanic_id'], ['mechanics.id'], name=op.f('fk_assistance_requests_mechanic_id_mechanics')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_assistance_requests_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assistance_request_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_payments_assistance_request_id_assistance_requests'), 'assistance_requests', ['assistance_request_id'], ['id'])

    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assistance_request_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_reviews_assistance_request_id_assistance_requests'), 'assistance_requests', ['assistance_request_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_reviews_assistance_request_id_assistance_requests'), type_='foreignkey')
        batch_op.drop_column('assistance_request_id')

    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_payments_assistance_request_id_assistance_requests'), type_='foreignkey')
        batch_op.drop_column('assistance_request_id')

    op.drop_table('assistance_requests')
    # ### end Alembic commands ###
