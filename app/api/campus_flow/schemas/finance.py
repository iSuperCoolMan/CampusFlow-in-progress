from datetime import datetime
from typing import Literal
from uuid import UUID

from app.api.campus_flow.schemas.base import BaseModelWithUUID


class Payment(BaseModelWithUUID):
    student_uuid: UUID
    amount: int
    due_date: datetime
    paid_date: datetime
    status: Literal["pending", "paid", "overdue"]
    method: str


class Scholarship(BaseModelWithUUID):
    student_uuid: UUID
    name: str
    amount: int
    start_date: datetime
    end_date: datetime