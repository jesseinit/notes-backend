import factory

from db.session import SessionLocal, get_db, DATABASE_URL, create_engine
from sqlalchemy import orm

Session = orm.scoped_session(orm.sessionmaker(bind=create_engine(DATABASE_URL)))


class BaseSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Always inherit from here"""

    class Meta:
        abstract = True  # Cannot initialize
        sqlalchemy_session = Session()
        sqlalchemy_session_persistence = "flush"
