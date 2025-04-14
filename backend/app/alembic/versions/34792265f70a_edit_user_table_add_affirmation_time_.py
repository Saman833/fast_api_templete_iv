"""edit user  table , add affirmation time and opted

Revision ID: 34792265f70a
Revises: 9e4aef07a42f
Create Date: 2025-04-14 11:35:43.386894

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '34792265f70a'
down_revision = '9e4aef07a42f'
branch_labels = None
depends_on = None

"""
affirmation_opted : bool = False
    affirmation_time: datetime.time | None = None  # Optional time-only field
"""

def upgrade():
    op.add_column('user', sa.Column('affirmation_opted', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('user', sa.Column('affirmation_time', sa.Time(), nullable=True))

def downgrade():
    op.drop_column('user', 'affirmation_time')
    op.drop_column('user', 'affirmation_opted')
