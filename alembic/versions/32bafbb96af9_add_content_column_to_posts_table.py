""" add content column to posts table

Revision ID: 32bafbb96af9
Revises: cf1c859e2537
Create Date: 2026-07-27 11:42:46.160685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32bafbb96af9'
down_revision: Union[str, Sequence[str], None] = 'cf1c859e2537'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
