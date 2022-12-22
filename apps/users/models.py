from sqlalchemy import Boolean, Column, String, event
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from db.base import Base


class Users(Base):

    ACTIVE_STATE = [
        ("ACTIVE", "ACTIVE"),
        ("BLOCKED", "BLOCKED"),
        ("ARCHIVED", "ARCHIVED"),
    ]

    username = Column(String(length=15), unique=True, index=True)
    first_name = Column(String(length=15))
    last_name = Column(String(length=15))
    email = Column(String)
    password = Column(String)
    status = Column(
        ChoiceType(ACTIVE_STATE, impl=String()),
        default=ACTIVE_STATE[0][0],
        nullable=False,
    )
    is_verified = Column(Boolean, default=True)
    notes = relationship("Notes", back_populates="owner")

    def __str__(self) -> str:
        return f"<Users username={self.username}>"

    def __repr__(self) -> str:
        return f"<Users username={self.username}>"


@event.listens_for(Users, "before_insert")
def update_user_password(mapper, connect, instance):
    from helpers.utils import HashManager

    instance.password = HashManager.hash_password(instance.password)
