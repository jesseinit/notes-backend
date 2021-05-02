# Import all the models, so that the Base class
# has them before being imported by Alembic.
from db.base import Base  # noqa
from apps.notes import models  # noqa
