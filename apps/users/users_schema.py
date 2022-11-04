from datetime import datetime
from enum import Enum
from typing import Optional, Union
from uuid import UUID

from pydantic import UUID4, BaseModel, Field


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    ARCHIVED = "ARCHIVED"


class UserLoginInputSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3, max_length=50)


class CreateUserInputSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3, max_length=50)


class CreatedUserSchema(BaseModel):
    id: UUID
    username: str
    first_name: str
    last_name: str
    email: str
    is_verified: bool
    status: Union[None, UserStatus]
    created_at: datetime
    updated_at: Union[None, datetime]
    deleted_at: Union[None, datetime]

    class Config:
        orm_mode = True
        use_enum_values = True


# class NoteSchema(BaseModel):
#     title: str = Field(..., min_length=3, max_length=50)
#     description: str = Field(..., min_length=3, max_length=1000000)


# class NoteResponse(NoteSchema):
#     id: UUID4
#     title: str = Field(..., min_length=3, max_length=50)
#     description: str = Field(..., min_length=3, max_length=1000000)
#     status: Union[None, NoteStatus]
#     created_at: datetime
#     updated_at: Union[None, datetime]
#     deleted_at: Union[None, datetime]

#     class Config:
#         orm_mode = True
#         use_enum_values = True


# class PatchNoteSchema(BaseModel):
#     title: Optional[str]
#     description: Optional[str]  # = Field(..., min_length=3, max_length=1000000)
#     status: Optional[NoteStatus]

#     # class Config:
#     #     orm_mode = True
#     #     use_enum_values = True
