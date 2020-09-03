"""empty message

Revision ID: a7855ad596d0
Revises: e6f9bc78a4b6
Create Date: 2020-09-03 18:27:55.454125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7855ad596d0'
down_revision = 'e6f9bc78a4b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('publish', sa.Boolean(), nullable=True, comment='公开'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'publish')
    # ### end Alembic commands ###
