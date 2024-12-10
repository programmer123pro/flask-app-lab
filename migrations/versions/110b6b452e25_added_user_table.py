"""Added user table

Revision ID: 110b6b452e25
Revises: e2753e6b70a8
Create Date: 2024-12-07 14:30:01.013216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '110b6b452e25'
down_revision = 'e2753e6b70a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('pasword', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###