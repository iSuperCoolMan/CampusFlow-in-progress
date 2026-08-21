import json
from pydantic_core import to_jsonable_python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .base import BaseORM
from app.api.auth.core.settings import db


engine = create_engine(
    db.DIRECTORY,
    echo=True,
    json_serializer=lambda obj: json.dumps(obj, default=to_jsonable_python)
)

BaseORM.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        return session