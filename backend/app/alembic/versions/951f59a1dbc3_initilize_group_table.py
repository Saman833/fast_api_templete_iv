"""initilize group table

Revision ID: 951f59a1dbc3
Revises: 9712bf24a95a
Create Date: 2025-04-13 14:08:38.265454

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

from sqlalchemy.dialects import postgresql
# revision identifiers, used by Alembic.
revision = '951f59a1dbc3'
down_revision = '9712bf24a95a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "group",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    pass
