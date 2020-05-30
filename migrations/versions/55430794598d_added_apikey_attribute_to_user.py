"""Added apikey attribute to User

Revision ID: 55430794598d
Revises: 8fa2825a3ed5
Create Date: 2020-05-31 00:20:55.337721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55430794598d'
down_revision = '8fa2825a3ed5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('apikey', sa.String(), default=''))


def downgrade():
    op.drop_column('user', 'apikey')
