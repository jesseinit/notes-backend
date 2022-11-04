from enum import Enum
from typing import Optional, Union
from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class NoteStatus(str, Enum):
    deleted = "DELETED"
    pubished = "PUBLISHED"
    draft = "DRAFT"
    archived = "ARCHIVED"


class CreateNoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=1000000)


class NoteResponse(BaseModel):
    id: UUID4
    title: str
    description: str
    status: Union[None, NoteStatus]
    created_at: datetime
    updated_at: Union[None, datetime]
    deleted_at: Union[None, datetime]

    class Config:
        orm_mode = True
        use_enum_values = True


class PatchNoteSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]  # = Field(..., min_length=3, max_length=1000000)
    status: Optional[NoteStatus]

    # class Config:
    #     orm_mode = True
    #     use_enum_values = True
