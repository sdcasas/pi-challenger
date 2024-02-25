import pytest
from factory.alchemy import SQLAlchemyModelFactory

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from settings.database import get_db, BaseDB


SQLALCHEMY_DATABASE_URL = "sqlite:///db/sqlite_testing.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def db_conf_testing():
    BaseDB.metadata.create_all(bind=engine)
    yield
    BaseDB.metadata.drop_all(bind=engine)


class BaseModelFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = TestingSessionLocal
        sqlalchemy_session_persistence = 'commit'


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
