"""

Revision ID: aa450eb26ec9
Revises: a8b5db702809
Create Date: 2023-07-11 00:30:18.488743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa450eb26ec9'
down_revision = 'a8b5db702809'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('items_owner_id_fkey', 'items', type_='foreignkey')
    op.create_foreign_key(None, 'items', 'users', ['owner_id'], [
                          'id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'items', type_='foreignkey')
    op.create_foreign_key('items_owner_id_fkey', 'items',
                          'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###