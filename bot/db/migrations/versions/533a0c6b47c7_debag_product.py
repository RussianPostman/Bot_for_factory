"""debag product

Revision ID: 533a0c6b47c7
Revises: f38dad332666
Create Date: 2023-03-07 17:07:50.001022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '533a0c6b47c7'
down_revision = 'f38dad332666'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('role', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
