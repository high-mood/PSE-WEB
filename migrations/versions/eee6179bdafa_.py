"""empty message

Revision ID: eee6179bdafa
Revises: 60423d1c5af4
Create Date: 2019-06-20 11:04:50.905962

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eee6179bdafa'
down_revision = '60423d1c5af4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songmoods', sa.Column('response_count', sa.Integer(), nullable=True))
    op.add_column('songmoods', sa.Column('response_excitedness', sa.Float(), nullable=True))
    op.add_column('songmoods', sa.Column('response_happiness', sa.Float(), nullable=True))
    op.drop_column('songmoods', 'responses_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songmoods', sa.Column('responses_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('songmoods', 'response_happiness')
    op.drop_column('songmoods', 'response_excitedness')
    op.drop_column('songmoods', 'response_count')
    # ### end Alembic commands ###
