from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.core.jwt_token import oauth2_scheme
from app.api.campus_flow.schemas.profile import ProfileUnion, profile_model_map, validate_profile_payload
from app.api.auth.core.settings import access_token as access_token_settings
from app.database import get_db
from app.database.crud import userCRUD
from app.database.crud.profile import profileCRUD_map
from app.utils.enums import RoleStr


router = APIRouter(
    tags=["people"],
    prefix="/people"
)


@router.post("/register")
async def register(
        role: RoleStr,
        profile_payload: ProfileUnion = Depends(validate_profile_payload),
        access_token = Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db)
):
    user = await userCRUD.get_by_token(db, access_token, access_token_settings)

    profile_payload.prepare_to_orm_model(user.uuid)

    profileCRUD = profileCRUD_map.get(role)

    try:
        profile = await profileCRUD.create(db, profile_payload, commit=True)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile is already exist"
        )

    RoleModel: BaseModel = profile_model_map.get(role)

    return RoleModel.model_validate(profile)

