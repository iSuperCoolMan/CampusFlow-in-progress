from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.core.security import get_password_hash
from app.database.models.auth import UserORM
from app.database.crud.base import BaseCRUD
from app.utils.validated_strings import Password


class UserCRUD(BaseCRUD[UserORM]):
    async def update_password(self, db: AsyncSession, user: UserORM, new_password: Password, commit: bool = False):
        user.hashed_password = get_password_hash(new_password)

        if commit:
            await db.commit()
        else:
            await db.flush()


userCRUD = UserCRUD()



