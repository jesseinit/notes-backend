from pydantic import UUID4, BaseModel, Field


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteResponse(NoteSchema):
    id: UUID4

    class Config:
        orm_mode = True
