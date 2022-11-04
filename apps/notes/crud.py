from datetime import datetime, timezone
from typing import List, Union

from pydantic.types import UUID4
from sqlalchemy import delete, select, update

from apps.notes.models import Notes as NotesModel
from apps.notes.notes_schema import CreateNoteSchema
from db.session import database, session


def create_new_note(payload: CreateNoteSchema, owner_id: UUID4) -> NotesModel:
    new_note = NotesModel(**payload.dict(), owner_id=str(owner_id))
    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    return new_note


def get_all_user_notes(owner) -> List[NotesModel]:
    all_notes = (
        session.query(NotesModel)
        .filter_by(owner=owner)
        .order_by(NotesModel.created_at.desc())
        .all()
    )
    return all_notes


def get_note_for_delete(note_id: UUID4, owner_id: UUID4) -> Union[None, NotesModel]:
    note = (
        session.query(NotesModel)
        .filter_by(id=note_id, owner_id=str(owner_id), deleted_at=None)
        .first()
    )
    return note


def get_note(note_id: UUID4, owner_id: UUID4) -> Union[None, NotesModel]:
    note = (
        session.query(NotesModel).filter_by(id=note_id, owner_id=str(owner_id)).first()
    )
    return note


def update_note(id: UUID4, payload: CreateNoteSchema, owner_id: UUID4) -> None:
    session.query(NotesModel).filter_by(id=id, owner_id=str(owner_id)).update(
        {**payload}
    )
    session.commit()
    return get_note(note_id=id, owner_id=owner_id)


def delete_note(note_id: UUID4, owner_id: UUID4) -> None:
    session.query(NotesModel).filter_by(
        id=note_id, owner_id=str(owner_id), deleted_at=None
    ).update(
        {
            "deleted_at": datetime.now(tz=timezone.utc),
            "status": NotesModel.NOTESTATE[0][1],
        }
    )
    session.commit()
