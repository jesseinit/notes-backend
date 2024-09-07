import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy_utils.functions import create_database, database_exists
from starlette.testclient import TestClient

from db.base import metadata
from main import app

import os


@pytest.fixture(autouse=True)
def set_env_vars():
    os.environ["TESTING"] = "True"


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Fixture that returns provisions the test database and tables"""
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")
    engine = create_engine(DATABASE_URL)
    if not database_exists(url=engine.url):
        create_database(url=engine.url)
    metadata.create_all(bind=engine)
    yield
    close_all_sessions()
    metadata.drop_all(bind=engine)


@pytest.fixture()
def test_app():
    """Fixture that returns the test app instance"""
    client = TestClient(app)
    yield client
