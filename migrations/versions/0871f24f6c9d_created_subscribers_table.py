"""created subscribers table

Revision ID: 0871f24f6c9d
Revises: edf152746247
Create Date: 2020-09-27 21:25:12.579186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0871f24f6c9d'
down_revision = 'edf152746247'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscribers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscribers_email'), 'subscribers', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subscribers_email'), table_name='subscribers')
    op.drop_table('subscribers')
    # ### end Alembic commands ###
