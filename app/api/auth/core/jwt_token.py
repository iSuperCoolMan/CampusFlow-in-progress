import asyncio

from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from .settings import TokenSettings
from ..schemas.token import TokenData


denylist = set()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(data: TokenData, settings: TokenSettings) -> str:
    encoded_jwt = jwt.encode(
        data.model_dump(),
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_token(token: Annotated[str, Depends(oauth2_scheme)], settings: TokenSettings) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenData.model_dump(payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_expire_delta_from_token(token: Annotated[str, Depends(oauth2_scheme)], settings: TokenSettings) -> datetime:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        expire = payload.get("exp")

        if expire is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return expire - datetime.now().timestamp()


async def revoke_token(token: Annotated[str, Depends(oauth2_scheme)], settings: TokenSettings) -> None:
    delta = get_expire_delta_from_token(token, settings)

    denylist.add(token)
    await asyncio.sleep(delta)
    denylist.remove(token)

