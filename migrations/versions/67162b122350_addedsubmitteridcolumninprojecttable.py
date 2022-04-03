"""AddedSubmitterIdColumnInProjectTable

Revision ID: 67162b122350
Revises:
Create Date: 2018-06-10 22:20:41.285468

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "67162b122350"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "project",
        sa.Column(
            "submitter_id",
            sa.Integer(),
            sa.ForeignKey("user.id"),
            nullable=True,
            default=None,
        ),
    )


def downgrade():
    op.drop_column("project", "submitter_id")
