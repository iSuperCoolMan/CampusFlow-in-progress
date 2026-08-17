import asyncio

from datetime import datetime, timezone, timedelta
from typing import Annotated, Literal

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from auth.core.settings import TokenSettings

denylist = set()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(data: dict, token_settings: TokenSettings) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=token_settings.EXPIRE_MINUTES)

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        token_settings.SECRET_KEY,
        algorithm=token_settings.ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str, token_settings: TokenSettings) -> dict[str: str]:
    try:
        payload = jwt.decode(token, token_settings.SECRET_KEY, algorithms=[token_settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_expire_delta_from_token(token: Annotated[str, Depends(oauth2_scheme)], token_settings: TokenSettings) -> datetime:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, token_settings.SECRET_KEY, algorithms=[token_settings.ALGORITHM])
        expire = payload.get("exp")

        if expire is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return expire - datetime.now().timestamp()


async def revoke_token(token: Annotated[str, Depends(oauth2_scheme)], role: Literal["access", "refresh"]) -> None:
    delta = get_expire_delta_from_token(token, role)

    denylist.add(token)
    await asyncio.sleep(delta)
    denylist.remove(token)

