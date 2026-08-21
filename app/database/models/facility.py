from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseORM


class RoomORM(BaseORM):
    campus_uuid: Mapped[UUID] = mapped_column(ForeignKey("campuses.uuid"))
    building: Mapped[int] = mapped_column()
    number: Mapped[int] = mapped_column()
    capacity: Mapped[int] = mapped_column()
    features: Mapped[dict[str, Any]] = mapped_column(JSON)


class RoomBookingORM(BaseORM):
    room_uuid: Mapped[UUID] = mapped_column(ForeignKey("rooms.uuid"))
    start: Mapped[datetime] = mapped_column()
    end: Mapped[datetime] = mapped_column()
    purpose: Mapped[str] = mapped_column()
    reserved_student_uuid: Mapped[UUID] = mapped_column(ForeignKey("students.uuid"))