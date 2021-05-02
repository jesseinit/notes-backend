"""add note state column

Revision ID: 2923a528cd73
Revises: b3d2819a2887
Create Date: 2021-05-02 15:04:34.124296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2923a528cd73"
down_revision = "b3d2819a2887"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    status_enum = postgresql.ENUM(
        "DELETED", "PUBLISHED", "DRAFT", "ARCHIVED", name="notestatus"
    )
    status_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "notes",
        sa.Column("status", status_enum, nullable=True),
    )
    # op.alter_column("notes", "status", nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("notes", "status")
    # ### end Alembic commands ###
