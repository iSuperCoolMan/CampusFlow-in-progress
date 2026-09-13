from typing import Any
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BaseORM


class BaseCRUD:
    model: type[BaseORM]


    def __init__(self, model: type(BaseORM)):
        self.model = model


    async def create(self, db: AsyncSession, pydantic_model: BaseModel, commit: bool = False) -> BaseORM:
        new_instance = self.model(**pydantic_model.model_dump())
        db.add(new_instance)

        if commit:
            await db.commit()
        else:
            await db.flush()

        await db.refresh(new_instance)

        return new_instance


    async def get_all(self, db: AsyncSession) -> list[BaseORM]:
        query = select(self.model)
        result = await db.execute(query)
        return result.scalars().all()


    async def get_one_or_none_by_uuid(self, db: AsyncSession, uuid: UUID) -> BaseORM:
        return await db.get(self.model, uuid)


    async def get_one_or_none_filtered(self, db: AsyncSession, filters: BaseModel, use_empty_fields: bool = False) -> BaseORM:
        filter_dict = filters.model_dump(exclude_unset=True, exclude_none=use_empty_fields)

        statement = select(self.model).filter_by(**filter_dict)
        scalars = await db.scalars(statement)
        return scalars.one_or_none()


    async def get_one_or_none_by_field(self, db: AsyncSession, field_name: str, value: Any) -> BaseORM:
        statement = select(self.model).where(getattr(self.model, field_name) == value)
        scalars = await db.scalars(statement)
        return scalars.one_or_none()


    async def update(
            self,
            db: AsyncSession,
            *to_update: list[BaseORM],
            update_fields: BaseModel,
            use_empty_fields: bool = False,
            commit: bool = False
    ):
        update_fields_dict = update_fields.model_dump(exclude_unset=True, exclude_none=use_empty_fields)

        for instance in to_update:
            for key, value in update_fields_dict:
                setattr(instance, key, value)

        if commit:
            await db.commit()
        else:
            await db.flush()

        for instance in to_update:
            await db.refresh(instance)


    async def delete(self, db: AsyncSession, *to_delete: list[BaseORM], commit: bool = False):
        for instance in to_delete:
            await db.delete(instance)

        if commit:
            await db.commit()
        else:
            await db.flush()

        for instance in to_delete:
            await db.refresh(instance)

