"""add user table

Revision ID: 21ce04cfc958
Revises: 6215419ba6d9
Create Date: 2024-04-26 15:15:03.415362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21ce04cfc958'
down_revision: Union[str, None] = '6215419ba6d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), nullable=False,primary_key=True),sa.Column("name",sa.String(),nullable=False),sa.Column("email",sa.String(),nullable=False),sa.Column("password",sa.String(),nullable=False),sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),sa.PrimaryKeyConstraint("id"),sa.UniqueConstraint("email")) 
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
