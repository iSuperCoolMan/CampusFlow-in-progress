from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.utils.enums import TokenRole
from app.api.auth.core.settings import access_token, refresh_token, email_token


class TokenData(BaseModel):
    sub: Any
    expire: datetime


class EmailTokenData(TokenData):
    sub: EmailStr
    expire: datetime = Field(default=datetime.now() + timedelta(minutes=email_token.EXPIRE_MINUTES))


class AccessTokenData(TokenData):
    sub: UUID
    expire: datetime = Field(default=datetime.now() + timedelta(minutes=access_token.EXPIRE_MINUTES))


class RefreshTokenData(TokenData):
    sub: UUID
    expire: datetime = Field(default=datetime.now() + timedelta(minutes=refresh_token.EXPIRE_MINUTES))


class Token(BaseModel):
    token: str
    role: TokenRole
    type: str = "bearer"