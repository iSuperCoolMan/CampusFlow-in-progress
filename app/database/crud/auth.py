from app.database.models.auth import UserORM
from app.database.crud.base import BaseCRUD


userCRUD = BaseCRUD(UserORM)



