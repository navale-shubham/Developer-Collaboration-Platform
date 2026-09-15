import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup():
    yield
    
    (Path('.') / 'tests' / 'temp_database.db').unlink(missing_ok=True)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
