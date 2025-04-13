"""edit group table, make id atugrenrated

Revision ID: 7e1f4a5db0f0
Revises: 951f59a1dbc3
Create Date: 2025-04-13 20:22:12.342267

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7e1f4a5db0f0'
down_revision = '951f59a1dbc3'
branch_labels = None
depends_on = None


def upgrade():
    # Ensure uuid-ossp extension is available
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create a new UUID column with a default UUID value
    op.add_column('group', sa.Column('new_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))

    # Populate the new columns with UUIDs
    op.execute('UPDATE "group" SET new_id = uuid_generate_v4()')

    # Set the new_id as not nullable
    op.alter_column('group', 'new_id', nullable=False)
 

    # Drop old columns and rename new columns

    op.drop_column('group', 'id')
    op.alter_column('group', 'new_id', new_column_name='id')


    # Create primary key constraint
    op.create_primary_key('group_pkey', 'group', ['id'])


def downgrade():
    pass
