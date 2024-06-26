"""record consent preferences

Revision ID: 39a23bc016ea
Revises: a0f219697fa0
Create Date: 2023-03-28 02:42:13.114938

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "39a23bc016ea"
down_revision = "a0f219697fa0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "consentrequest",
        sa.Column(
            "preferences", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    op.add_column(
        "consentrequest",
        sa.Column("identity_verified_at", sa.DateTime(timezone=True), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("consentrequest", "identity_verified_at")
    op.drop_column("consentrequest", "preferences")
    # ### end Alembic commands ###
