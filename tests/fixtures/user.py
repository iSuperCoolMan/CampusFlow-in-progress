import pytest

from app.api.auth.schemas.user import UserCreate

existing_users: list[UserCreate] = []


@pytest.fixture
def create_user():
    user = UserCreate(
        username=f"TestUser{len(existing_users) + 1}",
        email=f"testuser{len(existing_users) + 1}@test.com",
        password="testtest"
    )

    existing_users.append(user)

    return user


