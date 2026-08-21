from enum import Enum, StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import BaseORM


class BaseCRUD:
    model: BaseORM

    @classmethod
    async def add(cls, db: Session, pydantic_model: BaseModel) -> BaseORM:
        new_instance = cls.model(pydantic_model)
        db.add(new_instance)

        try:
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        return new_instance


    @classmethod
    async def get_all(cls, db: Session) -> list[BaseORM]:
        query = select(cls.model)
        result = db.execute(query)
        return result.scalars().all()


    @classmethod
    async def get_by_uuid(cls, db: Session, uuid: UUID) -> BaseORM:
        statement = select(cls.model).where(cls.model.uuid == uuid)
        return db.scalars(statement).one_or_none()


class BaseUniqueCRUD(BaseCRUD):
    unique_fields: StrEnum


    @classmethod
    async def get_by_unique_field(cls, db: Session, field: Any, field_name: StrEnum):
        column_name = field_name.value if isinstance(field_name, StrEnum) else field_name
        model_column = getattr(cls.model, column_name)
        statement = select(cls.model).where(model_column == field)
        return db.scalars(statement).one_or_none()
