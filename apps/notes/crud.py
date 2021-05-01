from typing import List, Union
from pydantic.types import UUID4
from db.session import session
from apps.notes.schema import NoteSchema
from apps.notes.models import Notes as NotesModel

from sqlalchemy.dialects.postgresql import UUID
from db.session import database


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
    from sqlalchemy import update

    query = (
        update(NotesModel)
        .where(NotesModel.id == id)
        .values(**payload.dict())
        .execution_options(synchronize_session="fetch")
    )

    return await database.execute(query=query)


async def delete(id: UUID4) -> None:
    from sqlalchemy import delete

    query = delete(NotesModel).where(NotesModel.id == id)
    return await database.execute(query=query)
