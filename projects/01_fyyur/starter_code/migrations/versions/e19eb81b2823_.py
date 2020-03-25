"""empty message

Revision ID: e19eb81b2823
Revises: a8b8088b5c36
Create Date: 2020-03-24 10:08:59.054647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e19eb81b2823'
down_revision = 'a8b8088b5c36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'artist_image_link')
    op.drop_column('Show', 'artist_name')
    op.drop_column('Show', 'venue_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('venue_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('artist_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('artist_image_link', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
