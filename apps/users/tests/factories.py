import factory

from apps.users.models import Users
from db.session import session


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Users
        sqlalchemy_session = session  # the SQLAlchemy session object

    # id = factory.Sequence(lambda n: n)
    # username = factory.Sequence(lambda n: "User %d" % n)
    # first_name = factory.Sequence(lambda n: "User %d" % n)
    # last_name = factory.Sequence(lambda n: "User %d" % n)
    # email = factory.Sequence(lambda n: "User %d" % n)
    # is_verified = factory.Boolen(lambda n: "User %d" % n)
    # email = factory.Sequence(lambda n: "User %d" % n)
