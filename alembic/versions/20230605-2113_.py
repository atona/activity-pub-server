"""empty message

Revision ID: b55a9bafc06a
Revises: 9e9f85491929
Create Date: 2023-06-05 21:13:57.097531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b55a9bafc06a'
down_revision = '9e9f85491929'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'display_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'display_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###