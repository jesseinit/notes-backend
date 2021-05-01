from uuid import uuid4

from db.base import Base
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID


class Notes(Base):
    title = Column(String)
    description = Column(Text)

    def __str__(self) -> str:
        return f"<NotesModel title={self.title}>"

    def __repr__(self) -> str:
        return f"<NotesModel title={self.title}>"
