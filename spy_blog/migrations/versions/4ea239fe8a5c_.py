"""empty message

Revision ID: 4ea239fe8a5c
Revises: ec13e656b5cc
Create Date: 2020-09-15 18:41:12.023092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ea239fe8a5c'
down_revision = 'ec13e656b5cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_role_ibfk_2', 'user_role', type_='foreignkey')
    op.drop_constraint('user_role_ibfk_1', 'user_role', type_='foreignkey')
    op.create_foreign_key(None, 'user_role', 'user', ['uid'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'user_role', 'role', ['rid'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_role', type_='foreignkey')
    op.drop_constraint(None, 'user_role', type_='foreignkey')
    op.create_foreign_key('user_role_ibfk_1', 'user_role', 'role', ['rid'], ['id'])
    op.create_foreign_key('user_role_ibfk_2', 'user_role', 'user', ['uid'], ['id'])
    # ### end Alembic commands ###
