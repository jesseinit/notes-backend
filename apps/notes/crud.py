from datetime import datetime, timezone
from typing import List, Union

from pydantic.types import UUID4

from apps.notes.models import Notes as NotesModel
from apps.notes.notes_schema import CreateNoteSchema
from db.session import get_db, SessionLocal as Session


def create_new_note(payload: CreateNoteSchema, owner_id: int, session: Session) -> NotesModel:
    new_note = NotesModel(**payload.dict(), owner_id=str(owner_id))
    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    return new_note


def get_all_user_notes(
    owner, page_number: int, page_size: int, session: Session
) -> List[NotesModel]:
    user_notes = (
        session.query(NotesModel)
        .filter_by(owner=owner, deleted_at=None)
        .order_by(NotesModel.created_at.desc())
    )
    total_count = user_notes.count()
    all_notes = user_notes.offset((page_number - 1) * page_size).limit(page_size).all()
    return all_notes, total_count


def get_note_for_delete(note_id: int, owner_id: int, session: Session) -> Union[None, NotesModel]:
    note = (
        session.query(NotesModel)
        .filter_by(id=note_id, owner_id=str(owner_id), deleted_at=None)
        .first()
    )
    return note


def get_note(note_id: int, owner_id: int, session: Session) -> Union[None, NotesModel]:
    note = (
        session.query(NotesModel)
        .filter_by(id=note_id, owner_id=str(owner_id), deleted_at=None)
        .first()
    )
    return note


def update_note(note_id: int, payload: CreateNoteSchema, owner_id: int, session: Session) -> None:
    session.query(NotesModel).filter_by(id=note_id, owner_id=str(owner_id), deleted_at=None).update(
        {**payload}
    )
    session.commit()
    return get_note(note_id=note_id, owner_id=owner_id, session=session)


def delete_note(note_id: int, owner_id: int, session: Session) -> None:
    session.query(NotesModel).filter_by(id=note_id, owner_id=str(owner_id), deleted_at=None).update(
        {
            "deleted_at": datetime.now(tz=timezone.utc),
            "status": NotesModel.NOTESTATE[0][1],
        }
    )
    session.commit()
