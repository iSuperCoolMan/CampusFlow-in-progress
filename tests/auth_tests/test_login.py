from unittest.mock import AsyncMock
from fastapi import status


def test_login_success(client, mock_user, monkeypatch):
    monkeypatch.setattr("app.api.auth.routers.base.get_user_by_username", lambda db, username: mock_user)
    monkeypatch.setattr("app.api.auth.routers.base.verify_password", lambda plain, hashed: True)

    monkeypatch.setattr("app.api.auth.routers.base.create_token", lambda data, settings: f"token_{settings}")

    form_data = {"username": "test_user", "password": "SecurePassword123"}
    response = client.post("/auth/login", data=form_data)

    assert response.status_code == 200
    tokens = response.json()
    assert len(tokens) == 2
    assert tokens[0]["role"] == "access"
    assert tokens[1]["role"] == "refresh"


def test_login_invalid_credentials(client, mock_user, monkeypatch):
    monkeypatch.setattr("app.api.auth.routers.base.get_user_by_username", lambda db, username: mock_user)
    monkeypatch.setattr("app.api.auth.routers.base.verify_password", lambda plain, hashed: False)

    form_data = {"username": "test_user", "password": "WrongPassword"}
    response = client.post("/auth/login", data=form_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid username or password"


def test_logout_success(client, monkeypatch):
    mock_revoke = AsyncMock()
    monkeypatch.setattr("app.api.auth.routers.base.revoke_token", mock_revoke)

    headers = {"Authorization": "Bearer token_to_revoke"}
    response = client.get("/auth/exit", headers=headers)

    assert response.status_code == 200
    assert response.json()["Message"] == "Logout successfully"