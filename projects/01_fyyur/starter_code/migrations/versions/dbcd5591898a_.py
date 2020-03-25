"""empty message

Revision ID: dbcd5591898a
Revises: c96ee16acc48
Create Date: 2020-03-22 23:39:47.578216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbcd5591898a'
down_revision = 'c96ee16acc48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Show', 'start_time',
               existing_type=sa.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Show', 'start_time',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
