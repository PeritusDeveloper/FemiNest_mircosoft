"""empty message

Revision ID: 92a07f1f15d5
Revises: d0f5045a746c
Create Date: 2022-05-29 20:02:26.900039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92a07f1f15d5'
down_revision = 'd0f5045a746c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('name', sa.String(length=100), nullable=True))
    op.add_column('contact', sa.Column('email', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contact', 'email')
    op.drop_column('contact', 'name')
    # ### end Alembic commands ###