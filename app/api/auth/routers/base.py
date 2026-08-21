from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas.user import UserCreate, UserResponse, Token

from ..core.settings import (
    email_token as email_token_settings,
    refresh_token as refresh_token_settings,
    access_token as access_token_settings
)

from ..core.email import send_verification_email
from ..core.security import verify_password
from ..core.jwt_token import revoke_token, oauth2_scheme, create_token, decode_token
from app.database.database import get_db
from app.database.crud.user import get_user_by_uuid, get_user_by_username, get_user_by_email, create_user


router = APIRouter(
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
        user_data: UserCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
):
    existing_user = get_user_by_username(db, username=user_data.username)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist."
        )

    existing_email = get_user_by_email(db, email=user_data.email)

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist."
        )

    new_user = create_user(db, user_data)

    token = create_token({"sub":new_user.email}, email_token_settings)
    background_tasks.add_task(send_verification_email, new_user.email, token)

    return new_user


@router.get("/verify-email")
def verify_email(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db),
):
    payload = decode_token(token, email_token_settings)
    email = payload["sub"]
    user = get_user_by_email(db, email)

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
        db: Session = Depends(get_db)
):
    user = get_user_by_username(db, username=form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    refresh_token = create_token({"sub": str(user.uuid)}, refresh_token_settings)
    access_token = create_token({"sub": str(user.uuid)}, access_token_settings)

    return [
        {
            "token": access_token,
            "role": "access",
            "type": "bearer"
        },
        {
            "token": refresh_token,
            "role": "refresh",
            "type": "bearer"
        }
    ]


@router.get(
    "/refresh", response_model=list[Token]
)
async def refresh(
        refresh_token = Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
):
    user_data = decode_token(refresh_token, "refresh")
    user_uuid = UUID(user_data["sub"])

    user = get_user_by_uuid(db, user_uuid)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    refresh_token = create_token({"sub": str(user.uuid)}, refresh_token_settings)
    access_token = create_token({"sub": str(user.uuid)}, access_token_settings)

    return [
        {
            "token": access_token,
            "role": "access",
            "type": "bearer"
        },
        {
            "token": refresh_token,
            "role": "refresh",
            "type": "bearer"
        }
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
