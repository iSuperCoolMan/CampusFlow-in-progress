from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.core.jwt_token import oauth2_scheme, decode_token
from app.api.campus_flow.schemas.people import PeoplePayload
from app.api.auth.core.settings import access_token as access_token_settings
from app.database import get_db
from app.database.crud import userCRUD

router = APIRouter(
    tags=["people"],
    prefix="/people"
)


@router.post("/register")
async def register(
        people_payload: PeoplePayload,
        access_token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db)
):
    user_uuid = decode_token(access_token, access_token_settings).sub
    user = await userCRUD.get_one_or_none_by_uuid(db, user_uuid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.role:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Role is already exist",
            headers={"role": f"{user.role}"},
        )

    data = people_payload.root

    userCRUD.update(db, user, )

