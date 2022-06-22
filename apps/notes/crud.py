from typing import List, Union

from pydantic.types import UUID4
from sqlalchemy import delete, select, update

from apps.notes.models import Notes as NotesModel
from apps.notes.notes_schema import NoteSchema
from db.session import database, session


def post(payload: NoteSchema) -> NotesModel:
    new_note = NotesModel(**payload.dict())
    session.add(new_note)
    session.commit()
    return new_note


def get_all() -> List[NotesModel]:
    all_notes = session.query(NotesModel).all()
    return all_notes


def get(id: UUID4) -> Union[None, NotesModel]:
    note = session.query(NotesModel).filter_by(id=id).first()
    return note


async def put(id: UUID4, payload: NoteSchema) -> None:
    query = update(NotesModel).where(NotesModel.id == id).values(**payload).execution_options(synchronize_session="fetch")
    return await database.execute(query=query)


async def delete(id: UUID4) -> None:
    query = delete(NotesModel).where(NotesModel.id == id)
    return await database.execute(query=query)
