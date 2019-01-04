"""update model for the news of projects

Revision ID: ca38dde2c84e
Revises: 71823751a67e
Create Date: 2019-01-03 23:54:45.262014

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca38dde2c84e'
down_revision = '71823751a67e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('feed',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('link', sa.String(), default=""),
            sa.Column('created_date', sa.DateTime(), default=datetime.utcnow),
            sa.Column('project_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['project_id'], ['project.id'],
                                    ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('entry_id', sa.String(), default=""),
            sa.Column('link', sa.String(), default=""),
            sa.Column('title', sa.String(), default=""),
            sa.Column('content', sa.String(), default=""),
            sa.Column('published', sa.DateTime(), default=datetime.utcnow),
            sa.Column('retrieved_date', sa.DateTime(), default=datetime.utcnow),
            sa.Column('project_id', sa.Integer(), nullable=False),
            sa.Column('feed_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['project_id'], ['project.id']),
            sa.ForeignKeyConstraint(['feed_id'], ['feed.id']),
            sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('feed')
    op.drop_table('article')
