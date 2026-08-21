import pytest

from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.api.main import app
from app.database.database import get_db


@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def client(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.username = "test_user"
    user.email = "test@campus.edu"
    user.hashed_password = "hashed_password_123"
    user.uuid = "12345678-1234-5678-1234-567812345678"
    user.is_verified = False
    return user