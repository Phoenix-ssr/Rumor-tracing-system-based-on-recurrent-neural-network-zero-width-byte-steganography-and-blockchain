"""add forecast and ifrumor

Revision ID: 00e632380c47
Revises: 86056907d070
Create Date: 2022-04-15 12:23:56.641503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00e632380c47'
down_revision = '86056907d070'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('ifrumor', sa.Integer(), nullable=True))
    op.add_column('article', sa.Column('forecast', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'forecast')
    op.drop_column('article', 'ifrumor')
    # ### end Alembic commands ###
