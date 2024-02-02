"""empty message

Revision ID: bd76dcc7c031
Revises: 306a642824bd
Create Date: 2024-02-02 11:55:03.695676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd76dcc7c031'
down_revision = '306a642824bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('token_expiration')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token_expiration', sa.DATETIME(), nullable=True))

    # ### end Alembic commands ###