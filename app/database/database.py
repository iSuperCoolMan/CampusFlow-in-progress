import asyncio
import json

from pydantic_core import to_jsonable_python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.database.models.base import BaseORM
from app.api.auth.core.settings import db


engine = create_async_engine(
    db.DIRECTORY,
    echo=True,
    json_serializer=lambda obj: json.dumps(obj, default=to_jsonable_python)
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)


async def get_db():
    async with AsyncSession(engine) as session:
        return session


asyncio.run(init_models())