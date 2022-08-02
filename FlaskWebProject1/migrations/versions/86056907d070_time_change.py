"""time change

Revision ID: 86056907d070
Revises: ecc628163870
Create Date: 2022-04-06 14:51:12.940244

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '86056907d070'
down_revision = 'ecc628163870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('time', mysql.VARCHAR(length=20), nullable=True))
    # ### end Alembic commands ###