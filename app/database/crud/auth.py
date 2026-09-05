from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.core.jwt_token import decode_token
from app.api.auth.core.security import get_password_hash
from app.api.auth.core.settings import TokenSettings
from app.database.models.auth import UserORM
from app.database.crud.base import BaseCRUD
from app.utils.validated_strings import PasswordStr


class UserCRUD(BaseCRUD[UserORM]):
    async def get_by_token(self, db: AsyncSession, token: str, token_settings: TokenSettings):
        user_uuid = decode_token(token, settings=token_settings).sub
        user = await self.get_one_or_none_by_uuid(db, user_uuid)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        return user


    async def update_password(self, db: AsyncSession, user: UserORM, new_password: PasswordStr, commit: bool = False):
        user.hashed_password = get_password_hash(new_password)

        if commit:
            await db.commit()
        else:
            await db.flush()


userCRUD = UserCRUD()



