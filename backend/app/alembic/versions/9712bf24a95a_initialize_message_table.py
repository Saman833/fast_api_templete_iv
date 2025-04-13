"""initialize message table

Revision ID: 9712bf24a95a
Revises: c535076eb5d2
Create Date: 2025-04-08 14:51:38.150524

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '9712bf24a95a'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chat",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sender_id", sa.UUID(), nullable=False),
        sa.Column("group_id", sa.UUID(), nullable=False),
        sa.Column("reploy_to", sa.Integer(), nullable=True),
        sa.Column("content", sa.String(length=255), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
    )
    


def downgrade():
    op.drop_table("chat")
