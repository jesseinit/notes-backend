from pydantic.types import UUID4
from db.session import session
from apps.notes.schema import NoteSchema
from apps.notes.models import Notes as NotesModel
from sqlalchemy.sql.expression import cast

from sqlalchemy.dialects.postgresql import UUID
from db.session import database


def post(payload: NoteSchema):
    new_note = NotesModel(**payload.dict())
    session.add(new_note)
    session.commit()
    return new_note


def get_all():
    all_notes = session.query(NotesModel).all()
    return all_notes


def get(id: UUID4):
    note = session.query(NotesModel).filter_by(id=id).first()
    return note


async def put(id: UUID4, payload: NoteSchema):
    from sqlalchemy import update

    query = (
        update(NotesModel)
        .where(NotesModel.id == id)
        .values(**payload.dict())
        .execution_options(synchronize_session="fetch")
    )

    # print("type", type(query))
    update_result = await database.execute(query=query)
    print("update_result>>>", update_result)
    return update_result


async def delete(id: int):
    query = Notes.delete().where(id == Notes.c.id)
    return await database.execute(query=query)
