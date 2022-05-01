"""changed table name 2

Revision ID: f8fcbe96bc4e
Revises: ae2032f26613
Create Date: 2022-05-01 12:28:10.871883

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f8fcbe96bc4e'
down_revision = 'ae2032f26613'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(length=80), nullable=True),
    sa.Column('user_name', sa.String(length=25), nullable=False),
    sa.Column('first_name', sa.String(length=373), nullable=False),
    sa.Column('last_name', sa.String(length=374), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('slug')
    )
    op.drop_table('signup users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('signup users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"signup users_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('slug', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('user_name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=373), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=374), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('date_added', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='signup users_pkey'),
    sa.UniqueConstraint('email', name='signup users_email_key'),
    sa.UniqueConstraint('slug', name='signup users_slug_key')
    )
    op.drop_table('my_users')
    # ### end Alembic commands ###
