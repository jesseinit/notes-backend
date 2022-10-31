from typing import List

from fastapi import APIRouter, HTTPException
from pydantic.types import UUID4

from apps.notes import crud
from apps.notes.notes_schema import NoteResponse, NoteSchema, PatchNoteSchema

router = APIRouter()


@router.post("", response_model=NoteResponse, status_code=201)
def create_note(payload: NoteSchema):
    new_note = crud.post(payload)
    return NoteResponse.from_orm(new_note)


@router.get("", response_model=List[NoteResponse])
def read_all_notes():
    all_notes = crud.get_all()
    return [NoteResponse.from_orm(note) for note in all_notes]


@router.get("/{id}", response_model=NoteResponse)
def read_note(id: UUID4):
    note = crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse.from_orm(note)


@router.patch("/{id}", response_model=NoteResponse)
async def patch_note(payload: PatchNoteSchema, id: UUID4):
    note = crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await crud.put(id, payload.dict(exclude_none=True))
    # TODO - Currently the get call to get note instance returns stale values. We have to figure a way to return the updated instance with a single call.
    note = crud.get(id)
    return NoteResponse.from_orm(note)


@router.delete("/{id}", response_model=NoteResponse)
async def delete_note(id: UUID4):
    note = crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)
    return NoteResponse.from_orm(note)
