"""init base tables

Revision ID: 547ffe58ab66
Revises: 
Create Date: 2024-01-18 18:03:24.343203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '547ffe58ab66'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.BIGINT(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'products',
        sa.Column('id', sa.BIGINT(), nullable=False),
        sa.Column('user_id', sa.BIGINT(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('price', sa.Integer(), default=0),
        sa.Column('category', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_foreign_key(
        'fk_products_user_id_users',
        'products', 'users',
        ['user_id'], ['id'],
    )


def downgrade() -> None:
    op.execute('DROP TABLE "users";')
    op.execute('DROP TABLE "products";')
