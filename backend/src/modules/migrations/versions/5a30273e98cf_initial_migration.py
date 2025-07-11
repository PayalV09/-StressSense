"""Initial migration

Revision ID: 5a30273e98cf
Revises: ecece5d1dc90
Create Date: 2025-04-09 18:05:30.021916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a30273e98cf'
down_revision = 'ecece5d1dc90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stress_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('mood', sa.String(length=50), nullable=True),
    sa.Column('sleep_hours', sa.Float(), nullable=True),
    sa.Column('coffee', sa.Boolean(), nullable=True),
    sa.Column('water_intake', sa.Float(), nullable=True),
    sa.Column('work_hours', sa.Float(), nullable=True),
    sa.Column('stress_level', sa.Float(), nullable=True),
    sa.Column('feelings', sa.Text(), nullable=True),
    sa.Column('activities', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('stress_record')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stress_record',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('stress_level', sa.FLOAT(), nullable=True),
    sa.Column('mood', sa.VARCHAR(length=50), nullable=True),
    sa.Column('sleep_hours', sa.FLOAT(), nullable=True),
    sa.Column('coffee', sa.INTEGER(), nullable=True),
    sa.Column('water_intake', sa.INTEGER(), nullable=True),
    sa.Column('activities', sa.VARCHAR(length=100), nullable=True),
    sa.Column('work_hours', sa.FLOAT(), nullable=True),
    sa.Column('feelings', sa.TEXT(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('stress_data')
    # ### end Alembic commands ###
