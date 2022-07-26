"""initial upgrade

Revision ID: 5b87634ecc7e
Revises: 
Create Date: 2022-07-26 17:41:03.244452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b87634ecc7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(length=128), nullable=True),
    sa.Column('user_name', sa.String(length=144), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.Column('bio', sa.String(length=400), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('blog_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('slug', sa.String(length=128), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_posts')
    op.drop_table('users')
    # ### end Alembic commands ###
