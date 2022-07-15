import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from apps.notes import notes_view as note_app

DATABASE_URL = os.environ["DATABASE_URL"]

from db.session import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(note_app.router, prefix="/notes", tags=["Notes Resource"])
