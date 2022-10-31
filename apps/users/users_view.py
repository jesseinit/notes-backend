from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from apps.users import crud
from apps.users.users_schema import CreatedUserSchema, CreateUserInputSchema

router = APIRouter()


@router.post("/auth/register", status_code=201)
def register_user(payload: CreateUserInputSchema):
    user = crud.get_existing_user(username=payload.username, email=payload.email)
    if user:
        return JSONResponse(
            content={"msg": "Username or Email has been taken", "data": None},
            status_code=409,
        )
    new_user = crud.create_user(payload)
    return {"msg": "Signup Successful", "data": CreatedUserSchema.from_orm(new_user)}


# @router.get("", response_model=List[NoteResponse])
# def read_all_notes():
#     all_notes = crud.get_all()
#     return [NoteResponse.from_orm(note) for note in all_notes]


# @router.get("/{id}", response_model=NoteResponse)
# def read_note(id: UUID4):
#     note = crud.get(id)
#     if not note:
#         raise HTTPException(status_code=404, detail="Note not found")
#     return NoteResponse.from_orm(note)


# @router.patch("/{id}", response_model=NoteResponse)
# async def patch_note(payload: PatchNoteSchema, id: UUID4):
#     note = crud.get(id)
#     if not note:
#         raise HTTPException(status_code=404, detail="Note not found")
#     await crud.put(id, payload.dict(exclude_none=True))
#     # TODO - Currently the get call to get note instance returns stale values. We have to figure a way to return the updated instance with a single call.
#     note = crud.get(id)
#     return NoteResponse.from_orm(note)


# @router.delete("/{id}", response_model=NoteResponse)
# async def delete_note(id: UUID4):
#     note = crud.get(id)
#     if not note:
#         raise HTTPException(status_code=404, detail="Note not found")

#     await crud.delete(id)
#     return NoteResponse.from_orm(note)
