"""create contest, problem, contest_problem, and problem_creators tables with UUIDs

Revision ID: 20250506_create_contest_and_problem_tables
Revises: 
Create Date: 2025-05-06

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = 'c4070e4a4664'
down_revision = 'fb360d92c6d4'
branch_labels = None
depends_on = None


def upgrade():
    # Create ENUM for difficulty levels
    difficulty_enum = sa.Enum('Easy', 'Medium', 'Hard', name='difficulty_levels')
    difficulty_enum.create(op.get_bind())

    # Create contest table
    op.create_table(
        'contest',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('start_time', sa.DateTime, nullable=False),
        sa.Column('end_time', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.sql.expression.true()),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    op.create_table(
        'problem',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False, unique=True),
        sa.Column('difficulty', difficulty_enum, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('input_format', sa.Text, nullable=True),
        sa.Column('output_format', sa.Text, nullable=True),
        sa.Column('sample_input', sa.Text, nullable=True),
        sa.Column('sample_output', sa.Text, nullable=True),
        sa.Column('constraints', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Create contest_problem join table
    op.create_table(
        'contest_problem',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4),
        sa.Column('contest_id', sa.UUID(as_uuid=True), sa.ForeignKey('contest.id', ondelete='CASCADE'), nullable=False),
        sa.Column('problem_id', sa.UUID(as_uuid=True), sa.ForeignKey('problem.id', ondelete='CASCADE'), nullable=False),
        sa.Column('display_order', sa.Integer, nullable=False),
        sa.Column('score', sa.Integer, nullable=True)
    )

    # Create problem_creators join table
    op.create_table(
        'problem_creators',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4),
        sa.Column('problem_id', sa.UUID(as_uuid=True), sa.ForeignKey('problem.id', ondelete='CASCADE'), nullable=False),
        sa.Column('creator_id', sa.UUID(as_uuid=True), nullable=False),  # FK to users table if defined
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('problem_creators')
    op.drop_table('contest_problem')
    op.drop_table('problem')
    op.drop_table('contest')
    op.execute('DROP TYPE IF EXISTS difficulty_levels')
