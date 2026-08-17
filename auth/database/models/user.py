from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from auth.database.models.base import Base


class UserORM(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()