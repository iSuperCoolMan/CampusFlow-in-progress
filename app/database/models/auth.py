import json

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import BaseORM
from app.utils.enums import VerifyServices
from app.utils.validated_strings import UsernameStr

default_verify_services = {service.value: False for service in VerifyServices}


class UserORM(BaseORM):
    role: Mapped[str] = mapped_column()
    username: Mapped[UsernameStr] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column()

    verify_services: Mapped[dict[VerifyServices, bool]] = mapped_column(
        JSON,
        default=lambda: dict(default_verify_services),
        server_default=f"'{json.dumps(default_verify_services)}'"
    )

    __mapper_args__ = {
        "polymorphic_on": "role",
        "polymorphic_identity": "user"
    }
