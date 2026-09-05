import pytest
import importlib
import asyncio

from sqlalchemy import NullPool

import app.database.database as db_module

from app.api.auth.core.settings import db
from app.database import get_db


TEST_DB_FILENAME = "database.db"


@pytest.fixture(scope="session", autouse=True)
def mock_db_settings():
    db.DIRECTORY = f"sqlite+aiosqlite:///{TEST_DB_FILENAME}"
    importlib.reload(db_module)

    db_module.engine.pool = NullPool(db_module.engine.pool._creator)

    yield


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mock_db():
    session = await get_db()
    try:
        yield session
    finally:
        await session.close()