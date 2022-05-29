"""empty message

Revision ID: 4356c00353c3
Revises: 1a40de8bf831
Create Date: 2022-05-29 19:53:19.498886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4356c00353c3'
down_revision = '1a40de8bf831'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('msg', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contact')
    # ### end Alembic commands ###
