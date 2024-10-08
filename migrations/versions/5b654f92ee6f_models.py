"""models

Revision ID: 5b654f92ee6f
Revises: 
Create Date: 2024-08-15 23:20:27.051031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b654f92ee6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reportdatas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('column1', sa.String(length=100), nullable=True),
    sa.Column('column2', sa.String(length=100), nullable=True),
    sa.Column('date_field', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('token_blocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_token_blocklist_jti'), ['jti'], unique=False)

    op.create_table('mechanics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=10), nullable=False),
    sa.Column('profile_picture', sa.String(length=255), nullable=True),
    sa.Column('expertise', sa.String(length=300), nullable=False),
    sa.Column('experience_years', sa.Integer(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admins.id'], name=op.f('fk_mechanics_admin_id_admins')),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], name=op.f('fk_mechanics_location_id_locations')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('username')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=10), nullable=False),
    sa.Column('profile_picture', sa.String(length=255), nullable=True),
    sa.Column('car_info', sa.String(length=300), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admins.id'], name=op.f('fk_users_admin_id_admins')),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], name=op.f('fk_users_location_id_locations')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('username')
    )
    op.create_table('assistance_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('mechanic_id', sa.Integer(), nullable=False),
    sa.Column('resolved', sa.Boolean(), nullable=True),
    sa.Column('message', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['mechanic_id'], ['mechanics.id'], name=op.f('fk_assistance_requests_mechanic_id_mechanics')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_assistance_requests_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=False),
    sa.Column('mechanic_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['mechanic_id'], ['mechanics.id'], name=op.f('fk_services_mechanic_id_mechanics')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('visits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_visits_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_user_id', sa.Integer(), nullable=True),
    sa.Column('receiver_user_id', sa.Integer(), nullable=True),
    sa.Column('sender_mechanic_id', sa.Integer(), nullable=True),
    sa.Column('receiver_mechanic_id', sa.Integer(), nullable=True),
    sa.Column('assistance_request_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['assistance_request_id'], ['assistance_requests.id'], name=op.f('fk_notifications_assistance_request_id_assistance_requests')),
    sa.ForeignKeyConstraint(['receiver_mechanic_id'], ['mechanics.id'], name=op.f('fk_notifications_receiver_mechanic_id_mechanics')),
    sa.ForeignKeyConstraint(['receiver_user_id'], ['users.id'], name=op.f('fk_notifications_receiver_user_id_users')),
    sa.ForeignKeyConstraint(['sender_mechanic_id'], ['mechanics.id'], name=op.f('fk_notifications_sender_mechanic_id_mechanics')),
    sa.ForeignKeyConstraint(['sender_user_id'], ['users.id'], name=op.f('fk_notifications_sender_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('mechanic_id', sa.Integer(), nullable=True),
    sa.Column('assistance_request_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assistance_request_id'], ['assistance_requests.id'], name=op.f('fk_payments_assistance_request_id_assistance_requests')),
    sa.ForeignKeyConstraint(['mechanic_id'], ['mechanics.id'], name=op.f('fk_payments_mechanic_id_mechanics')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_payments_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('feedback', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('mechanic_id', sa.Integer(), nullable=False),
    sa.Column('assistance_request_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assistance_request_id'], ['assistance_requests.id'], name=op.f('fk_reviews_assistance_request_id_assistance_requests')),
    sa.ForeignKeyConstraint(['mechanic_id'], ['mechanics.id'], name=op.f('fk_reviews_mechanic_id_mechanics')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_reviews_user_id_users')),
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
    op.drop_table('reviews')
    op.drop_table('payments')
    op.drop_table('notifications')
    op.drop_table('visits')
    op.drop_table('services')
    op.drop_table('assistance_requests')
    op.drop_table('users')
    op.drop_table('mechanics')
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_blocklist_jti'))

    op.drop_table('token_blocklist')
    op.drop_table('reportdatas')
    op.drop_table('locations')
    op.drop_table('admins')
    # ### end Alembic commands ###
