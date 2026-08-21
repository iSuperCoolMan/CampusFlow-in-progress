from unittest.mock import AsyncMock
from fastapi import status


def test_register_success(client, mock_user, monkeypatch):
    monkeypatch.setattr("app.api.auth.routers.base.get_user_by_username", lambda db, username: None)
    monkeypatch.setattr("app.api.auth.routers.base.get_user_by_email", lambda db, email: None)
    monkeypatch.setattr("app.api.auth.routers.base.create_user", lambda db, data: mock_user)

    monkeypatch.setattr("app.api.auth.routers.base.create_token", lambda data, settings: "fake_email_token")
    mock_send_email = AsyncMock()
    monkeypatch.setattr("app.api.auth.routers.base.send_verification_email", mock_send_email)

    payload = {
        "username": "test_user",
        "email": "test@campus.edu",
        "password": "SecurePassword123"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "test_user"


def test_register_duplicate_username(client, mock_user, monkeypatch):
    monkeypatch.setattr("app.api.auth.routers.base.get_user_by_username", lambda db, username: mock_user)

    payload = {"username": "test_user", "email": "new@campus.edu", "password": "Password123"}
    response = client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User with this username already exist."