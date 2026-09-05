from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.enums import TokenRole
from ..schemas.user import UserCreate, User, UserSoftDelete
from ..schemas.token import Token, EmailTokenData, RefreshTokenData, AccessTokenData

from ..core.settings import (
    email_token as email_token_settings,
    refresh_token as refresh_token_settings,
    access_token as access_token_settings
)

from ..core.email import send_verification_email
from ..core.security import verify_password
from ..core.jwt_token import revoke_token, oauth2_scheme, create_token, decode_token
from app.database.database import get_db
from app.database.crud import userCRUD


router = APIRouter(
    tags=["auth"],
    prefix="/auth"
)


@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
async def register(
        user_data: UserCreate,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db),
):
    existing_username = await userCRUD.get_one_or_none_by_field(db, "username", user_data.username)

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist."
        )

    existing_email = await userCRUD.get_one_or_none_by_field(db, "email", user_data.email)

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist."
        )

    new_user = await userCRUD.create(db, user_data, commit=True)

    token = create_token(EmailTokenData(sub=new_user.email), email_token_settings)
    background_tasks.add_task(send_verification_email, new_user.email, token)

    return new_user


@router.get("/verify-email")
async def verify_email(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db),
):
    email = decode_token(token, email_token_settings).sub
    user = await userCRUD.get_one_or_none_by_field(db, "email", email)

    if user:
        if user.is_verified:
            return {"Message": "Email is already verified."}

        user.is_verified = True
        return {"Message": "Email successfully verified! You can now log in."}

    raise HTTPException(status_code=404, detail="User not found")


@router.post(
    "/login",
    response_model=list[Token]
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    user = await userCRUD.get_one_or_none_by_field(db, "username", form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    refresh_token = create_token(RefreshTokenData(sub=user.uuid), refresh_token_settings)
    access_token = create_token(AccessTokenData(sub=user.uuid), access_token_settings)

    return [
        Token(token=access_token, role=TokenRole.access),
        Token(token=refresh_token, role=TokenRole.refresh)
    ]


@router.get(
    "/refresh", response_model=list[Token]
)
async def refresh(
        refresh_token = Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db)
):
    user_uuid = decode_token(refresh_token, "refresh").sub
    user = await userCRUD.get_one_or_none_by_uuid(db, user_uuid)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    refresh_token = create_token(RefreshTokenData(sub=user.uuid), refresh_token_settings)
    access_token = create_token(AccessTokenData(sub=user.uuid), access_token_settings)

    return [
        Token(token=access_token, role=TokenRole.access),
        Token(token=refresh_token, role=TokenRole.refresh)
    ]


@router.get("/exit")
async def logout(
        background_tasks: BackgroundTasks,
        access_token = Annotated[str, Depends(oauth2_scheme)],
        refresh_token = Annotated[str, Depends(oauth2_scheme)]
):
    background_tasks.add_task(revoke_token, access_token)
    background_tasks.add_task(revoke_token, refresh_token)

    return {
        "Message": "Logout successfully"
    }


@router.get("/delete/soft")
async def soft_delete(
        db: AsyncSession = Depends(get_db),
        access_token = Annotated[str, Depends(oauth2_scheme)]
):
    user_uuid = decode_token(access_token, settings=access_token_settings).sub
    user = await userCRUD.get_one_or_none_by_uuid(db, user_uuid)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    await userCRUD.update(db, user, UserSoftDelete(), commit=True)

    return {
        "Message": f"User {user.username} is inactive."
    }


@router.get("/delete/hard")
async def hard_delete(
        db: AsyncSession = Depends(get_db),
        access_token = Annotated[str, Depends(oauth2_scheme)]
):
    user_uuid = decode_token(access_token, settings=access_token_settings).sub
    user = await userCRUD.get_one_or_none_by_uuid(db, user_uuid)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    await userCRUD.delete(db, user, commit=True)

    return {
        "Message": f"User {user.username} was deleted."
    }
