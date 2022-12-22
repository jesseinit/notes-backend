import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if os.getenv("TESTING"):
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    # except Exception:
    #     session.rollback()
    finally:
        db.close()
