"""Added Notes and User Tables

Revision ID: a15e562c82fd
Revises: 
Create Date: 2022-12-18 07:59:09.027024

"""
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "a15e562c82fd"
down_revision = None
branch_labels = None
depends_on = None
from apps.notes.models import Notes
from apps.users.models import Users


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("username", sa.String(length=15), nullable=True),
        sa.Column("first_name", sa.String(length=15), nullable=True),
        sa.Column("last_name", sa.String(length=15), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column(
            "status",
            sqlalchemy_utils.types.choice.ChoiceType(
                Users.ACTIVE_STATE, impl=sa.String()
            ),
            nullable=False,
        ),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sqlalchemy_utils.types.choice.ChoiceType(Notes.NOTESTATE, impl=sa.String()),
            nullable=False,
        ),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], name=op.f("fk_notes_owner_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notes")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notes")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###