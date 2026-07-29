"""add foreign key to post table

Revision ID: 7c9e6087b247
Revises: 480048ebd638
Create Date: 2026-07-27 12:22:28.303655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c9e6087b247'
down_revision: Union[str, Sequence[str], None] = '480048ebd638'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
