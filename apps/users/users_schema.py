from datetime import datetime
from enum import Enum
from typing import Optional, Union
from uuid import UUID

from pydantic import UUID4, BaseModel, EmailStr, Field


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
    email: EmailStr
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
