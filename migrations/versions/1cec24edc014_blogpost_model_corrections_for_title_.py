"""blogpost model corrections for title and slug

Revision ID: 1cec24edc014
Revises: 854e07e8b07d
Create Date: 2022-07-12 17:06:42.870950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cec24edc014'
down_revision = '854e07e8b07d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('blog_posts', 'title',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    op.alter_column('blog_posts', 'slug',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('blog_posts', 'image',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('blog_posts', 'description',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    op.create_unique_constraint(None, 'blog_posts', ['title'])
    op.create_unique_constraint(None, 'blog_posts', ['slug'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'blog_posts', type_='unique')
    op.drop_constraint(None, 'blog_posts', type_='unique')
    op.alter_column('blog_posts', 'description',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    op.alter_column('blog_posts', 'image',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('blog_posts', 'slug',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('blog_posts', 'title',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    # ### end Alembic commands ###
