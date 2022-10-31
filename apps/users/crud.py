from typing import Union

from sqlalchemy import delete, insert, or_, select, update

from apps.users.models import Users as UsersModel
from apps.users.users_schema import CreateUserInputSchema
from db.session import database, session


def create_user(payload: CreateUserInputSchema) -> UsersModel:
    new_user = UsersModel(**payload.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_existing_user(username: str, email: str) -> Union[None, UsersModel]:
    user = (
        session.query(UsersModel)
        .filter(or_(UsersModel.username == username, UsersModel.email == email))
        .first()
    )
    return user
