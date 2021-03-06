"""create notes model

Revision ID: 4dd69d034ded
Revises:
Create Date: 2021-05-03 17:01:31.476148

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = "4dd69d034ded"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    NOTESTATE = [
        ("DELETED", "DELETED"),
        ("PUBLISHED", "PUBLISHED"),
        ("DRAFT", "DRAFT"),
        ("ARCHIVED", "ARCHIVED"),
    ]
    op.create_table(
        "notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sqlalchemy_utils.types.choice.ChoiceType(
                choices=NOTESTATE, impl=sa.String()
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notes_id"), "notes", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_notes_id"), table_name="notes")
    op.drop_table("notes")
    # ### end Alembic commands ###
