import re

from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, ConfigDict

from app.api.auth.core.security import get_password_hash
from app.utils.enums import VerifyServices
from app.utils.validated_strings import Username, Password


class UserCreate(BaseModel):
    username: Username
    email: EmailStr
    password: Password
    is_active: bool = True
    verify_services: dict[VerifyServices, bool] = {service: False for service in VerifyServices}


    def generate_user_model(self) -> "User":
        return User(
            uuid=uuid4(),
            username=self.username,
            email=self.email,
            hashed_password=get_password_hash(self.password),
            verify_services=self.verify_services
        )


class UserSoftDelete(BaseModel):
    is_active: bool = False


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    username: Username
    email: str
    hashed_password: str
    is_active: bool
    verify_services: dict[VerifyServices, bool]
