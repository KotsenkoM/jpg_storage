"""initial
Revision ID: fc07cb68f919
Revises:
Create Date: 2024-03-03 22:35:11.832830
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc07cb68f919'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'pictures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint('unique_name_constraint', 'pictures', ['name'])


def downgrade() -> None:
    op.drop_table('pictures')
    op.drop_constraint('unique_name_constraint', 'pictures')
