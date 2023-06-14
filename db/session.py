import os
import socket

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from helpers.logger import logger

if os.getenv("TESTING"):
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=True,
    connect_args={"application_name": f"host>>{socket.gethostname()}"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.info("DB Closed")
