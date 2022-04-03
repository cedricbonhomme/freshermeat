"""Add new tables for the submissions

Revision ID: 71823751a67e
Revises: 14ddbf5ff3cd
Create Date: 2018-09-02 22:30:25.134310

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "71823751a67e"
down_revision = "14ddbf5ff3cd"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "submission",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_name", sa.String(), default=""),
        sa.Column("project_description", sa.String(), default=""),
        sa.Column("project_website", sa.String(), default=""),
        sa.Column("reviewed", sa.Boolean(), default=False),
        sa.Column("accepted", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "association_submissions_licenses",
        sa.Column("submission_id", sa.Integer(), sa.ForeignKey("submission.id")),
        sa.Column("license_id", sa.Integer(), sa.ForeignKey("license.id")),
    )


def downgrade():
    op.drop_table("association_submissions_licenses")
    op.drop_table("submission")
