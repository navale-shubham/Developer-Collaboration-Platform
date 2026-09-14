import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup():
    db_path = Path(".") / "tests" / "database" / "temp.db"

    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.touch(exist_ok=True)

    yield

    db_path.unlink(missing_ok=True)
    db_path.parent.rmdir()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
