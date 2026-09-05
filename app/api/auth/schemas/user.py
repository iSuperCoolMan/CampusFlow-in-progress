import re

from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, ConfigDict

from app.api.auth.core.security import get_password_hash
from app.utils.enums import VerifyServices, Role
from app.utils.validated_strings import UsernameStr, PasswordStr


class UserCreate(BaseModel):
    username: UsernameStr
    email: EmailStr
    password: PasswordStr
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


class UserUpdate(BaseModel):
    username: UsernameStr | None
    email: EmailStr | None


class UserSoftDelete(BaseModel):
    is_active: bool = False


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    username: UsernameStr
    email: EmailStr
    hashed_password: str
    is_active: bool
    verify_services: dict[VerifyServices, bool]
