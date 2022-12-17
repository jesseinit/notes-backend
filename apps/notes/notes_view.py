import math
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, Response
from fastapi_pagination import LimitOffsetPage, Page, Params, paginate
from pydantic.types import UUID4

from apps.notes import crud
from apps.notes.notes_schema import CreateNoteSchema, NoteResponse, PatchNoteSchema
from helpers.utils import JWTBearer

router = APIRouter()


@router.post("", response_model=NoteResponse, status_code=201)
def create_note(
    payload: CreateNoteSchema, current_user: JWTBearer = Depends(JWTBearer())
):
    new_note = crud.create_new_note(payload, owner_id=current_user.id)
    return NoteResponse.from_orm(new_note)


@router.get("")
def read_all_notes(
    page_number: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Page size"),
    current_user: JWTBearer = Depends(JWTBearer()),
):
    all_notes, all_notes_count_before_offset = crud.get_all_user_notes(
        current_user, page_number=page_number, page_size=page_size
    )
    return {
        "msg": "Notes Retrieved",
        "data": [NoteResponse.from_orm(note) for note in all_notes],
        "meta": {"total_notes": all_notes_count_before_offset},
    }


@router.get("/{id}")
def read_note(id: UUID4, current_user: JWTBearer = Depends(JWTBearer())):
    note = crud.get_note(note_id=id, owner_id=current_user.id)
    if not note:
        return JSONResponse(
            content={
                "msg": "Notes not found.",
                "data": None,
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )
    return {
        "msg": "Notes retreived.",
        "data": NoteResponse.from_orm(note),
    }


@router.patch("/{id}")
def patch_note(
    payload: PatchNoteSchema, id: UUID4, current_user: JWTBearer = Depends(JWTBearer())
):
    note = crud.get_note(note_id=id, owner_id=current_user.id)
    if not note:
        return JSONResponse(
            content={
                "msg": "Notes not found.",
                "data": None,
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )
    note = crud.update_note(
        id, payload.dict(exclude_none=True), owner_id=current_user.id
    )
    return {
        "msg": "Notes retreived.",
        "data": NoteResponse.from_orm(note),
    }


@router.delete("/{id}", status_code=204)
def delete_note(id: UUID4, current_user: JWTBearer = Depends(JWTBearer())):
    note = crud.get_note_for_delete(note_id=id, owner_id=current_user.id)
    if not note:
        return JSONResponse(
            content={
                "msg": "Notes not found.",
                "data": None,
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )
    crud.delete_note(note_id=id, owner_id=current_user.id)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
