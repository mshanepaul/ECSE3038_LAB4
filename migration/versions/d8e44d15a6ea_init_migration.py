"""init migration
Revision ID: d8e44d15a6ea
Revises: 
Create Date: 2021-02-26 23:08:25.890512
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8e44d15a6ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tanks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('long', sa.Float(), nullable=False),
    sa.Column('percentage_full', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tanks')
    # ### end Alembic commands ###
