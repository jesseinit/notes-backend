import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from helpers.logger import logger

DATABASE_URL = os.getenv("DATABASE_URL_TEST") if os.getenv("TESTING") else os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        logger.info("Session Opened")
        yield db
    finally:
        db.close()
        logger.info("Session Closed")
