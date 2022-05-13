"""add content column to posts table

Revision ID: 78b6ed72a583
Revises: d9d4a613464e
Create Date: 2022-05-12 22:59:35.115775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78b6ed72a583'
down_revision = 'd9d4a613464e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
