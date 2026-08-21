from datetime import datetime
from typing import Any
from uuid import UUID

from app.api.campus_flow.schemas.base import BaseModelWithUUID


class Room(BaseModelWithUUID):
    campus_uuid: UUID
    building: int
    number: int
    capacity: int
    features: dict[str, Any]


class RoomBooking(BaseModelWithUUID):
    room_uuid: UUID
    start: datetime
    end: datetime
    purpose: str
    reserved_student_uuid: UUID