import factory
from db.session import session


class BaseSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Always inherit from here"""

    class Meta:
        abstract = True  # Cannot initialize
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "flush"
