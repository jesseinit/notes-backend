import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

load_dotenv()

from apps.notes import notes_view as note_app
from apps.users import users_view as user_app

DATABASE_URL = os.environ["DATABASE_URL"]

from db.session import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"msg": f"Oops! {str(exc)}", "data": None},
    )


app.include_router(user_app.router, prefix="/v1/users", tags=["Users Resource"])
app.include_router(note_app.router, prefix="/v1/notes", tags=["Notes Resource"])
