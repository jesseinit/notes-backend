import factory
from faker import Faker

import base_tests_factory as base_factory
from apps.users.models import Users


class UserFactory(base_factory.BaseSQLAlchemyModelFactory):
    class Meta:
        model = Users

    id = factory.Sequence(lambda n: n)
    username = factory.LazyFunction(lambda: Faker().user_name())
    first_name = factory.LazyFunction(lambda: Faker().first_name())
    last_name = factory.LazyFunction(lambda: Faker().first_name())
    email = factory.LazyFunction(lambda: Faker().email())
    password = factory.LazyFunction(lambda: Faker().password())
    status = factory.LazyFunction(
        lambda: Faker().random_element([state[1] for state in Users.ACTIVE_STATE])
    )
    is_verified = factory.LazyFunction(lambda: Faker().boolean())
