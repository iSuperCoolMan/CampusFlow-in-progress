from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import BaseORM


class MaintenanceRequestORM(BaseORM):
    campus_uuid: Mapped[UUID] = mapped_column(ForeignKey("campuses.uuid"))
    room_uuid: Mapped[UUID] = mapped_column(ForeignKey("rooms.uuid"), nullable=True)
    description: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    requested_on: Mapped[datetime] = mapped_column()
    resolved_on: Mapped[datetime] = mapped_column()
    vendor_uuid: Mapped[UUID] = mapped_column(ForeignKey("vendors.uuid"))


class VendorORM(BaseORM):
    name: Mapped[str] = mapped_column()
    contact_email: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()