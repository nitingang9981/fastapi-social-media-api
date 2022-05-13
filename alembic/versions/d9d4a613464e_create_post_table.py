"""create post table

Revision ID: d9d4a613464e
Revises: 
Create Date: 2022-05-12 22:45:54.688380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9d4a613464e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(),nullable=False, primary_key=True), sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
