# Import all the models, so that Base has them before being
# imported by Alembic

from app.db.base_class import Base  # noqa
from app.models.item import DBItem  # noqa
from app.models.user import DBUser  # noqa
