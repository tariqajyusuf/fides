"""add_tcf_columns

Revision ID: cba3118c0ab5
Revises: 5abb65a8cb91
Create Date: 2023-07-18 21:13:24.855078

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cba3118c0ab5"
down_revision = "5abb65a8cb91"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "consentsettings",
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
        sa.Column("tcf_enabled", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_consentsettings_id"), "consentsettings", ["id"], unique=False
    )
    op.add_column(
        "currentprivacypreference", sa.Column("data_use", sa.String(), nullable=True)
    )
    op.add_column(
        "currentprivacypreference", sa.Column("feature", sa.String(), nullable=True)
    )
    op.add_column(
        "currentprivacypreference", sa.Column("tcf_version", sa.String(), nullable=True)
    )
    op.add_column(
        "currentprivacypreference", sa.Column("vendor", sa.String(), nullable=True)
    )
    op.alter_column(
        "currentprivacypreference",
        "privacy_notice_id",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "currentprivacypreference",
        "privacy_notice_history_id",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.create_unique_constraint(
        "fides_user_device_identity_data_use",
        "currentprivacypreference",
        ["fides_user_device_provided_identity_id", "data_use"],
    )
    op.create_unique_constraint(
        "fides_user_device_identity_feature",
        "currentprivacypreference",
        ["fides_user_device_provided_identity_id", "feature"],
    )
    op.create_unique_constraint(
        "fides_user_device_identity_vendor",
        "currentprivacypreference",
        ["fides_user_device_provided_identity_id", "vendor"],
    )
    op.create_unique_constraint(
        "identity_data_use",
        "currentprivacypreference",
        ["provided_identity_id", "data_use"],
    )
    op.create_unique_constraint(
        "identity_feature",
        "currentprivacypreference",
        ["provided_identity_id", "feature"],
    )
    op.create_unique_constraint(
        "identity_vendor",
        "currentprivacypreference",
        ["provided_identity_id", "vendor"],
    )
    op.create_index(
        op.f("ix_currentprivacypreference_data_use"),
        "currentprivacypreference",
        ["data_use"],
        unique=False,
    )
    op.create_index(
        op.f("ix_currentprivacypreference_feature"),
        "currentprivacypreference",
        ["feature"],
        unique=False,
    )
    op.create_index(
        op.f("ix_currentprivacypreference_vendor"),
        "currentprivacypreference",
        ["vendor"],
        unique=False,
    )
    op.add_column("lastservednotice", sa.Column("data_use", sa.String(), nullable=True))
    op.add_column("lastservednotice", sa.Column("feature", sa.String(), nullable=True))
    op.add_column(
        "lastservednotice", sa.Column("tcf_version", sa.String(), nullable=True)
    )
    op.add_column("lastservednotice", sa.Column("vendor", sa.String(), nullable=True))
    op.alter_column(
        "lastservednotice",
        "privacy_notice_id",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "lastservednotice",
        "privacy_notice_history_id",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.create_index(
        op.f("ix_lastservednotice_data_use"),
        "lastservednotice",
        ["data_use"],
        unique=False,
    )
    op.create_index(
        op.f("ix_lastservednotice_feature"),
        "lastservednotice",
        ["feature"],
        unique=False,
    )
    op.create_index(
        op.f("ix_lastservednotice_vendor"), "lastservednotice", ["vendor"], unique=False
    )
    op.add_column(
        "privacypreferencehistory", sa.Column("data_use", sa.String(), nullable=True)
    )
    op.add_column(
        "privacypreferencehistory", sa.Column("feature", sa.String(), nullable=True)
    )
    op.add_column(
        "privacypreferencehistory", sa.Column("vendor", sa.String(), nullable=True)
    )
    op.add_column(
        "privacypreferencehistory", sa.Column("tcf_version", sa.String(), nullable=True)
    )
    op.alter_column(
        "privacypreferencehistory",
        "privacy_notice_history_id",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.create_index(
        op.f("ix_privacypreferencehistory_data_use"),
        "privacypreferencehistory",
        ["data_use"],
        unique=False,
    )
    op.create_index(
        op.f("ix_privacypreferencehistory_feature"),
        "privacypreferencehistory",
        ["feature"],
        unique=False,
    )
    op.create_index(
        op.f("ix_privacypreferencehistory_vendor"),
        "privacypreferencehistory",
        ["vendor"],
        unique=False,
    )
    op.add_column(
        "servednoticehistory", sa.Column("data_use", sa.String(), nullable=True)
    )
    op.add_column(
        "servednoticehistory", sa.Column("feature", sa.String(), nullable=True)
    )
    op.add_column(
        "servednoticehistory", sa.Column("vendor", sa.String(), nullable=True)
    )
    op.add_column(
        "servednoticehistory", sa.Column("tcf_version", sa.String(), nullable=True)
    )
    op.alter_column(
        "servednoticehistory",
        "privacy_notice_history_id",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.create_index(
        op.f("ix_servednoticehistory_data_use"),
        "servednoticehistory",
        ["data_use"],
        unique=False,
    )
    op.create_index(
        op.f("ix_servednoticehistory_feature"),
        "servednoticehistory",
        ["feature"],
        unique=False,
    )
    op.create_index(
        op.f("ix_servednoticehistory_vendor"),
        "servednoticehistory",
        ["vendor"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        op.f("ix_servednoticehistory_vendor"), table_name="servednoticehistory"
    )
    op.drop_index(
        op.f("ix_servednoticehistory_feature"), table_name="servednoticehistory"
    )
    op.drop_index(
        op.f("ix_servednoticehistory_data_use"), table_name="servednoticehistory"
    )

    op.drop_column("servednoticehistory", "tcf_version")
    op.drop_column("servednoticehistory", "vendor")
    op.drop_column("servednoticehistory", "feature")
    op.drop_column("servednoticehistory", "data_use")
    op.drop_index(
        op.f("ix_privacypreferencehistory_vendor"),
        table_name="privacypreferencehistory",
    )
    op.drop_index(
        op.f("ix_privacypreferencehistory_feature"),
        table_name="privacypreferencehistory",
    )
    op.drop_index(
        op.f("ix_privacypreferencehistory_data_use"),
        table_name="privacypreferencehistory",
    )

    op.drop_column("privacypreferencehistory", "tcf_version")
    op.drop_column("privacypreferencehistory", "vendor")
    op.drop_column("privacypreferencehistory", "feature")
    op.drop_column("privacypreferencehistory", "data_use")
    op.drop_index(op.f("ix_lastservednotice_vendor"), table_name="lastservednotice")
    op.drop_index(op.f("ix_lastservednotice_feature"), table_name="lastservednotice")
    op.drop_index(op.f("ix_lastservednotice_data_use"), table_name="lastservednotice")

    op.drop_column("lastservednotice", "vendor")
    op.drop_column("lastservednotice", "tcf_version")
    op.drop_column("lastservednotice", "feature")
    op.drop_column("lastservednotice", "data_use")
    op.drop_index(
        op.f("ix_currentprivacypreference_vendor"),
        table_name="currentprivacypreference",
    )
    op.drop_index(
        op.f("ix_currentprivacypreference_feature"),
        table_name="currentprivacypreference",
    )
    op.drop_index(
        op.f("ix_currentprivacypreference_data_use"),
        table_name="currentprivacypreference",
    )
    op.drop_constraint("identity_vendor", "currentprivacypreference", type_="unique")
    op.drop_constraint("identity_feature", "currentprivacypreference", type_="unique")
    op.drop_constraint("identity_data_use", "currentprivacypreference", type_="unique")
    op.drop_constraint(
        "fides_user_device_identity_vendor", "currentprivacypreference", type_="unique"
    )
    op.drop_constraint(
        "fides_user_device_identity_feature", "currentprivacypreference", type_="unique"
    )
    op.drop_constraint(
        "fides_user_device_identity_data_use",
        "currentprivacypreference",
        type_="unique",
    )

    op.drop_column("currentprivacypreference", "vendor")
    op.drop_column("currentprivacypreference", "tcf_version")
    op.drop_column("currentprivacypreference", "feature")
    op.drop_column("currentprivacypreference", "data_use")
    op.drop_index(op.f("ix_consentsettings_id"), table_name="consentsettings")
    op.drop_table("consentsettings")
