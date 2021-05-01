from typing import List

from fastapi import APIRouter, HTTPException, Path
from pydantic.types import UUID4

from apps.notes import crud
from apps.notes.schema import NoteDB, NoteResponse, NoteSchema


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


@router.put("/{id}", response_model=NoteDB)
async def update_note(payload: NoteSchema, id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await crud.put(id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return note
