import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database, database_exists, drop_database
from starlette.testclient import TestClient

from main import app


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Fixture that returns provisions the test database and tables"""
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    if database_exists(url=engine.url):
        drop_database(url=engine.url)
    create_database(url=engine.url)
    from db.base import metadata

    metadata.create_all(bind=engine)
    yield
    if database_exists(engine.url):
        drop_database(url=engine.url)


@pytest.fixture()
def test_app():
    """Fixture that returns the test app instance"""
    client = TestClient(app)
    yield client
