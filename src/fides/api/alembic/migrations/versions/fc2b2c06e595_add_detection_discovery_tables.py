"""add detection discovery tables

Revision ID: fc2b2c06e595
Revises: d873e3e430b0
Create Date: 2024-04-25 19:53:59.562332

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fc2b2c06e595"
down_revision = "d873e3e430b0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Staged resource table
    op.create_table(
        "stagedresource",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("urn", sa.String(), nullable=False),
        sa.Column("resource_type", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("monitor_config_id", sa.String(), nullable=True),
        sa.Column("source_modified", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "classifications",
            sa.ARRAY(postgresql.JSONB(astext_type=sa.Text())),
            server_default="{}",
            nullable=False,
        ),
        sa.Column(
            "user_assigned_data_categories",
            sa.ARRAY(sa.String()),
            server_default="{}",
            nullable=False,
        ),
        sa.Column(
            "children", sa.ARRAY(sa.String()), server_default="{}", nullable=False
        ),
        sa.Column("parent", sa.String(), nullable=True),
        sa.Column("diff_status", sa.String(), nullable=True),
        sa.Column(
            "child_diff_statuses",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default="{}",
            nullable=False,
        ),
        sa.Column(
            "meta",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default="{}",
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_stagedresource_id"), "stagedresource", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_stagedresource_urn"), "stagedresource", ["urn"], unique=True
    )
    op.create_index(
        op.f("ix_stagedresource_resource_type"),
        "stagedresource",
        ["resource_type"],
        unique=False,
    )

    # Monitor config table
    op.create_table(
        "monitorconfig",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("connection_config_id", sa.String(), nullable=False),
        sa.Column(
            "classify_params", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["connection_config_id"],
            ["connectionconfig.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_monitorconfig_id"), "monitorconfig", ["id"], unique=False)
    op.create_index(op.f("ix_monitorconfig_key"), "monitorconfig", ["key"], unique=True)
    op.create_index(
        op.f("ix_monitorconfig_connection_config_id"),
        "monitorconfig",
        ["connection_config_id"],
        unique=False,
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Staged resource table
    op.drop_index(op.f("ix_stagedresource_resource_type"), table_name="stagedresource")
    op.drop_index(op.f("ix_stagedresource_urn"), table_name="stagedresource")
    op.drop_index(op.f("ix_stagedresource_id"), table_name="stagedresource")
    op.drop_table("stagedresource")

    # Monitor config table
    op.drop_index(op.f("ix_monitorconfig_id"), table_name="monitorconfig")
    op.drop_index(op.f("ix_monitorconfig_key"), table_name="monitorconfig")
    op.drop_index(
        op.f("ix_monitorconfig_connection_config_id"), table_name="monitorconfig"
    )
    op.drop_table("monitorconfig")
    # ### end Alembic commands ###
