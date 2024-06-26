"""dashboard sharing

Revision ID: 9b589bf91485
Revises: decc96c5670f
Create Date: 2021-09-10 10:24:37.018830

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b589bf91485'
down_revision = 'decc96c5670f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dashboardshare', sa.Column('status', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('share_object', 'environmentUri', existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column('dashboardshare', 'status')
    # ### end Alembic commands ###
