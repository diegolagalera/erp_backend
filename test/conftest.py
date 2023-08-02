from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from config.database import Base, db_connection
import pytest

TEST_DATABASE_URL = "postgresql://erp:123456@localhost:5432/test_erp_db"
main_app = app    # this app comes from my main file, in which i declared FAST API as app


def start_application():   # start application
    return main_app


SQLALCHEMY_DATABASE_URL = TEST_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)  # create engine

# now we create test-session
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app():
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)    # drop that tables


@pytest.fixture(scope="function")
def db_session(app: FastAPI):
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: SessionTesting):
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        db_session = SessionTesting()
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[db_connection] = _get_test_db
    with TestClient(app) as client:
        yield client
