"""Add property id to privacy request model

Revision ID: a3c173391603
Revises: 5fe01e730171
Create Date: 2024-06-04 17:40:35.230801

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a3c173391603"
down_revision = "5fe01e730171"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "privacyrequest", sa.Column("property_id", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("privacyrequest", "property_id")
    # ### end Alembic commands ###
