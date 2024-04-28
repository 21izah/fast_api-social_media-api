"""add last few columns to posts table

Revision ID: 4a1aafb4a772
Revises: 1992a0c0c5c0
Create Date: 2024-04-26 15:34:17.462224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a1aafb4a772'
down_revision: Union[str, None] = '1992a0c0c5c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("published", sa.Boolean(),  nullable=False, server_default="TRUE"))
    op.add_column("posts",sa.Column("created_at", sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
