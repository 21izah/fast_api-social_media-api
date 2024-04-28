"""add reset token  column to users table

Revision ID: 2c43158404da
Revises: 97676c1bd78c
Create Date: 2024-04-27 02:12:01.657661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c43158404da'
down_revision: Union[str, None] = '97676c1bd78c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users",sa.Column("reset_token", sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("users","reset_token")
    pass
