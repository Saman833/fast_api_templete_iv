"""initlize affirmation table

Revision ID: 9e4aef07a42f
Revises: 7e1f4a5db0f0
Create Date: 2025-04-14 11:29:45.325676

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '9e4aef07a42f'
down_revision = '7e1f4a5db0f0'
branch_labels = None
depends_on = None

"""

class AffirmationBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    content: Optional[str] = Field(default=None, max_length=255)

# SQLModel-based DB table
class Affirmation(AffirmationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
"""
def upgrade():
    op.create_table(
        "affirmation",
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("content", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table(
        "affirmation"
    )
