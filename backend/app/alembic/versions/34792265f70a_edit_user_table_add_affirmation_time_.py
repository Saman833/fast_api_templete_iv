"""edit user table , add affirmation time and opted

Revision ID: 34792265f70a
Revises: 9e4aef07a42f
Create Date: 2025-04-14 11:35:43.386894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34792265f70a'
down_revision = '9e4aef07a42f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('affirmation_opted', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('user', sa.Column('affirmation_schedule', sa.Time(), nullable=True))


def downgrade():
    op.drop_column('user', 'affirmation_schedule')
    op.drop_column('user', 'affirmation_opted')
