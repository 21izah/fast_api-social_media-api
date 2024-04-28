"""add content column to posts table

Revision ID: 6215419ba6d9
Revises: 52d0d3d7fec8
Create Date: 2024-04-26 15:01:28.533900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6215419ba6d9'
down_revision: Union[str, None] = '52d0d3d7fec8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
