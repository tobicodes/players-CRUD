"""create traits table

Revision ID: 394335503f3a
Revises: 41283e8c73c8
Create Date: 2017-05-20 16:05:39.559482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '394335503f3a'
down_revision = '41283e8c73c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('traits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('traits')
    # ### end Alembic commands ###
