import socket

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError

load_dotenv()

import logging
from logging import config as loggin_config

from apps.notes import notes_view as note_app
from apps.users import users_view as user_app

app = FastAPI(title="Notes API")

import yaml

# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/issues/19#issuecomment-1039405731
with open("logging.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    loggin_config.dictConfig(config)

logger = logging.getLogger("CORE")
logger.info("CORE started!")


@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"msg": f"Oops! Validation Error Occured", "data": exc.errors()},
    )


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "msg": f"Oops! {str(exc)}",
            "data": None,
            "host": socket.gethostname(),
        },
    )


@app.get("/", status_code=200, tags=["Home"])
def index():
    logger.info("Index Page")
    return {"msg": "The App is Running", "data": None, "host": socket.gethostname()}


@app.get("/health", status_code=200, tags=["Home"])
def health():
    return {"msg": "The App is Running", "data": None}


app.include_router(user_app.router, prefix="/v1/user", tags=["Users Resource"])
app.include_router(note_app.router, prefix="/v1/note", tags=["Notes Resource"])
