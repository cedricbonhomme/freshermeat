"""Removed the table service

Revision ID: 8fa2825a3ed5
Revises: ca38dde2c84e
Create Date: 2019-08-25 14:42:15.555968

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "8fa2825a3ed5"
down_revision = "ca38dde2c84e"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("request")
    op.drop_table("service")
