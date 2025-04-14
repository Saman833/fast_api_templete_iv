"""initilize user_addrimation table

Revision ID: ebb3f08f1047
Revises: 34792265f70a
Create Date: 2025-04-14 11:39:49.643417

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ebb3f08f1047'
down_revision = '34792265f70a'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "user_affirmation",
        sa.Column("affirmation_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("status", sa.String(length=10), nullable=False),
    )

def downgrade():
    op.drop_table("user_affirmation")
