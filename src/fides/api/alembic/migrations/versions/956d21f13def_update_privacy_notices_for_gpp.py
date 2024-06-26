"""update privacy notices for gpp

Revision ID: 956d21f13def
Revises: 61a922702f4c
Create Date: 2024-01-10 02:14:24.802051

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "956d21f13def"
down_revision = "61a922702f4c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "privacynotice",
        sa.Column(
            "gpp_field_mapping", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    op.add_column(
        "privacynotice",
        sa.Column("framework", sa.String(), nullable=True),
    )
    op.alter_column("privacynotice", "data_uses", server_default="{}")

    op.add_column(
        "privacynoticehistory",
        sa.Column(
            "gpp_field_mapping", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    op.add_column(
        "privacynoticehistory",
        sa.Column("framework", sa.String(), nullable=True),
    )
    op.alter_column("privacynoticehistory", "data_uses", server_default="{}")

    op.add_column(
        "privacynoticetemplate",
        sa.Column(
            "gpp_field_mapping", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    op.add_column(
        "privacynoticetemplate",
        sa.Column("framework", sa.String(), nullable=True),
    )
    op.alter_column("privacynoticetemplate", "data_uses", server_default="{}")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("privacynoticetemplate", "gpp_field_mapping")
    op.drop_column("privacynoticetemplate", "framework")
    op.drop_column("privacynoticehistory", "gpp_field_mapping")
    op.drop_column("privacynoticehistory", "framework")
    op.drop_column("privacynotice", "gpp_field_mapping")
    op.drop_column("privacynotice", "framework")
    # ### end Alembic commands ###
