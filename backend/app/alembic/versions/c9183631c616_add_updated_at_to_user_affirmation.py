"""add updated_at to user_affirmation

Revision ID: c9183631c616
Revises: ebb3f08f1047
Create Date: 2025-04-16 01:44:24.726397

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c9183631c616'
down_revision = 'ebb3f08f1047'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column(
        'user_affirmation',
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

def downgrade():
    op.drop_column('user_affirmation', 'updated_at')
