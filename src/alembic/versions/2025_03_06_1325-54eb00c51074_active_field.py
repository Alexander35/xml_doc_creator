"""active field

Revision ID: 54eb00c51074
Revises: 274d70a37a2a
Create Date: 2025-03-06 13:25:05.108508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54eb00c51074'
down_revision: Union[str, None] = '274d70a37a2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document', 'active')
    # ### end Alembic commands ###
