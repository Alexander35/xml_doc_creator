"""initial

Revision ID: 274d70a37a2a
Revises: 
Create Date: 2025-03-06 13:05:23.291711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '274d70a37a2a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document',
    sa.Column('reportingEntityId', sa.String(), nullable=False),
    sa.Column('reportingEntityIdType', sa.Enum('ace', 'lei', 'bic', 'eic', 'gln', name='entityidtype'), nullable=False),
    sa.Column('recordSeqNumber', sa.Integer(), nullable=False),
    sa.Column('idOfMarketParticipant', sa.String(), nullable=False),
    sa.Column('idOfMarketParticipantType', sa.Enum('ace', 'lei', 'bic', 'eic', 'gln', name='entityidtype'), nullable=False),
    sa.Column('otherMarketParticipant', sa.String(), nullable=False),
    sa.Column('otherMarketParticipantType', sa.Enum('ace', 'lei', 'bic', 'eic', 'gln', name='entityidtype'), nullable=False),
    sa.Column('tradingCapacity', sa.Enum('P', 'A', name='tradingcapacitytype'), nullable=False),
    sa.Column('buySellIndicator', sa.Enum('B', 'S', 'C', name='buysellindicatortype'), nullable=False),
    sa.Column('contractId', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document')
    # ### end Alembic commands ###
