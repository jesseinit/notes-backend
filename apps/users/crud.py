from typing import Union

from sqlalchemy import or_

from apps.users.models import Users as UsersModel
from apps.users.users_schema import CreateUserInputSchema
from db.session import SessionLocal


def create_user(payload: CreateUserInputSchema) -> UsersModel:
    with SessionLocal() as session:
        new_user = UsersModel(**payload.dict())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user


def get_existing_user(username: str, email: str) -> Union[None, UsersModel]:
    with SessionLocal() as session:
        user = (
            session.query(UsersModel)
            .filter(or_(UsersModel.username == username, UsersModel.email == email))
            .first()
        )
        return user


def get_user_by_username(username: str) -> Union[None, UsersModel]:
    with SessionLocal() as session:
        user = session.query(UsersModel).filter_by(username=username).first()
        return user
