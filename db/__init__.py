# Import all the models, so that the Base class
# has them before being imported by Alembic.
from apps.notes import models  # noqa
from db.base import Base  # noqa
