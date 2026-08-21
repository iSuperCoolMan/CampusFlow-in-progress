from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseORM
from app.utils.enums import VerifyServices


class UserORM(BaseORM):
    type: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()

    verify_services: Mapped[dict[VerifyServices, bool]] = mapped_column(
        JSON,
        default=lambda: {service.value: False for service in VerifyServices},
        server_default=lambda: {service.value: False for service in VerifyServices}
    )

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "user"
    }
