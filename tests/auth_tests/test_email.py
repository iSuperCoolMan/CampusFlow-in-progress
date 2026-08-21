def test_verify_email_success(client, mock_user, monkeypatch):
    monkeypatch.setattr("app.api.auth.routers.base.decode_token", lambda token, settings: {"sub": "test@campus.edu"})
    monkeypatch.setattr("app.api.auth.routers.base.get_user_by_email", lambda db, email: mock_user)

    mock_user.is_verified_email = False

    headers = {"Authorization": "Bearer fake_token"}
    response = client.get("/auth/verify-email", headers=headers)

    assert response.status_code == 200
    assert mock_user.is_verified_email is True
    assert "successfully verified" in response.json()["Message"]