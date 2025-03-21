"""Add phone_number column

Revision ID: 1783dadda477
Revises: f57af0b6c281
Create Date: 2024-12-09 22:10:49.359393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1783dadda477'
down_revision: Union[str, None] = 'f57af0b6c281'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(length=15), nullable=True))
    op.create_unique_constraint('uq_user_email', 'users', ['email'])
    op.create_unique_constraint('uq_user_username', 'users', ['username'])
    op.create_unique_constraint(None, 'users', ['phone_number'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint('uq_user_username', 'users', type_='unique')
    op.drop_constraint('uq_user_email', 'users', type_='unique')
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
