"""Add a new association table for the dependencies.

Revision ID: 14ddbf5ff3cd
Revises: 67162b122350
Create Date: 2018-08-11 17:10:46.712729

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "14ddbf5ff3cd"
down_revision = "67162b122350"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "association_projects_projects",
        sa.Column("project_dependent_id", sa.Integer(), sa.ForeignKey("project.id")),
        sa.Column("project_dependency_id", sa.Integer(), sa.ForeignKey("project.id")),
    )


def downgrade():
    op.drop_table("association_projects_projects")
