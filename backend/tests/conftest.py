import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient
from pathlib import Path

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup():
    DATABASE_URL = Path('.') / 'tests' / 'temp_database.db'

    with patch("app.config.DATABASE_URL", DATABASE_URL):
        yield
    
    DATABASE_URL.unlink()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
