import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

if os.getenv("TESTING"):
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
# engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    with SessionLocal() as db:
        yield db
    # except Exception:
    #     session.rollback()
    # finally:
    #     db.close()


# session = next(get_db())
# session = SessionLocal()
