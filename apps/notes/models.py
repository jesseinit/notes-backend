from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base


class Notes(Base):

    NOTESTATE = [
        ("DELETED", "DELETED"),
        ("PUBLISHED", "PUBLISHED"),
        ("DRAFT", "DRAFT"),
        ("ARCHIVED", "ARCHIVED"),
    ]

    title = Column(String)
    description = Column(Text)
    status = Column(
        ChoiceType(NOTESTATE, impl=String()),
        default=NOTESTATE[1][0],
        nullable=False,
    )
    owner_id = Column(UUID, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="notes")

    def __str__(self) -> str:
        return f"<NotesModel title={self.title}>"

    def __repr__(self) -> str:
        return f"<NotesModel title={self.title}>"
