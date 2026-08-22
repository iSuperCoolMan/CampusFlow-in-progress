from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BaseORM


class BaseCRUD:
    model: type[BaseORM]


    def __init__(self, model: type[BaseORM]):
        self.model = model


    async def add(self, db: AsyncSession, pydantic_model: BaseModel) -> BaseORM:
        new_instance = pydantic_model.model_validate(pydantic_model)
        db.add(new_instance)
        await db.flush()
        return new_instance


    async def get_all(self, db: AsyncSession) -> list[BaseORM]:
        query = select(self.model)
        result = await db.execute(query)
        return result.scalars().all()


    async def get_one_or_none_by_uuid(self, db: AsyncSession, uuid: UUID):
        return await db.get(self.model, uuid)


    async def get_one_or_none(self, db: AsyncSession, filters: BaseModel, use_empty_fields: bool = False) -> BaseORM:
        filter_dict = filters.model_dump(exclude_unset=True, exclude_none=use_empty_fields)

        statement = select(self.model).filter_by(**filter_dict)
        scalars = await db.scalars(statement)
        return scalars.one_or_none()


    async def update(self, db: AsyncSession, *to_update: list[type[T]], update_fields: BaseModel, use_empty_fields: bool = False):
        update_fields_dict = update_fields.model_dump(exclude_unset=True, exclude_none=use_empty_fields)

        for instance in to_update:
            for key, value in update_fields_dict:
                setattr(instance, key, value)

        await db.flush()


    async def delete(self, db: AsyncSession, *to_delete: list[type[T]]):
        for instance in to_delete:
            await db.delete(instance)