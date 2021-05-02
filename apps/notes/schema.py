from enum import Enum
from typing import Union

from pydantic import UUID4, BaseModel, Field


class NoteStatus(str, Enum):
    deleted = "deleted"
    pubished = "pubished"
    draft = "draft"
    archived = "archived"


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteResponse(NoteSchema):
    id: UUID4
    status: Union[None, NoteStatus]

    class Config:
        orm_mode = True
        use_enum_values = True
