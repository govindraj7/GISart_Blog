"""added BlogPosts model

Revision ID: 854e07e8b07d
Revises: da0eb276815b
Create Date: 2022-07-05 14:24:02.365135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '854e07e8b07d'
down_revision = 'da0eb276815b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_posts')
    # ### end Alembic commands ###
