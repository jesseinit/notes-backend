import factory

from db.session import get_db


class BaseSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Always inherit from here"""

    class Meta:
        abstract = True  # Cannot initialize
        sqlalchemy_session = next(get_db())
        sqlalchemy_session_persistence = "flush"
