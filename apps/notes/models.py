import enum
from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType

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
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), default=None, nullable=True)

    def __str__(self) -> str:
        return f"<NotesModel title={self.title}>"

    def __repr__(self) -> str:
        return f"<NotesModel title={self.title}>"
