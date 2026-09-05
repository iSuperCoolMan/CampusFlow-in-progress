import pytest

from app.api.auth.schemas.user import User
from app.database.crud import userCRUD
from tests.fixtures.user import existing_users


@pytest.mark.asyncio
async def test_create_user(mock_db, create_user, monkeypatch):
    assert await userCRUD.create(mock_db, create_user)
    await mock_db.commit()

    with pytest.raises(Exception):
        user = await userCRUD.create(mock_db, create_user)
        await mock_db.commit()
        assert not user


@pytest.mark.asyncio
async def test_get_users(mock_db, create_user, monkeypatch):
    user = await userCRUD.create(mock_db, create_user)
    await mock_db.commit()

    assert await userCRUD.get_one_or_none_by_uuid(mock_db, user.uuid)
    assert await userCRUD.get_one_or_none_by_field(mock_db, "username", user.username)
    assert await userCRUD.get_one_or_none_by_field(mock_db, "email", user.email)
    assert await userCRUD.get_one_or_none_filtered(mock_db, User.model_validate(user))

    users = await userCRUD.get_all(mock_db)

    assert [left.username == right.username for left, right in ([user for user in users], [user for user in existing_users])]


@pytest.mark.asyncio
async def test_update_user(mock_db, create_user, monkeypatch):
    user = await userCRUD.create(mock_db, create_user)
    await mock_db.commit()

    assert userCRUD.update(mock_db, user)
