"""empty message

Revision ID: 5b183ae4e6b0
Revises: 
Create Date: 2022-05-27 14:33:26.890753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b183ae4e6b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('driver', sa.Column('driverid', sa.String(length=50), nullable=False))
    op.add_column('driver', sa.Column('phone', sa.String(length=10), nullable=False))
    op.add_column('driver', sa.Column('aadhar', sa.String(length=12), nullable=False))
    op.add_column('driver', sa.Column('vehicle', sa.String(length=30), nullable=False))
    op.alter_column('driver', 'name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.create_unique_constraint(None, 'driver', ['phone'])
    op.create_unique_constraint(None, 'driver', ['vehicle'])
    op.create_unique_constraint(None, 'driver', ['aadhar'])
    op.drop_column('driver', 'VehicleNo')
    op.drop_column('driver', 'AadharNo')
    op.drop_column('driver', 'id')
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.add_column('driver', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('driver', sa.Column('AadharNo', sa.INTEGER(), nullable=True))
    op.add_column('driver', sa.Column('VehicleNo', sa.VARCHAR(length=30), nullable=True))
    op.drop_constraint(None, 'driver', type_='unique')
    op.drop_constraint(None, 'driver', type_='unique')
    op.drop_constraint(None, 'driver', type_='unique')
    op.alter_column('driver', 'name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.drop_column('driver', 'vehicle')
    op.drop_column('driver', 'aadhar')
    op.drop_column('driver', 'phone')
    op.drop_column('driver', 'driverid')
    # ### end Alembic commands ###
