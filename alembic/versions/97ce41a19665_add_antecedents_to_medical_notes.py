"""add antecedents to medical notes

Revision ID: 97ce41a19665
Revises: b65db5bf6b0f
Create Date: 2026-07-05 18:37:44.359696

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "97ce41a19665"
down_revision: Union[str, Sequence[str], None] = "b65db5bf6b0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "medical_notes",
        sa.Column(
            "antecedents",
            sa.Text(),
            nullable=False,
            server_default=""
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "medical_notes",
        "antecedents"
    )
