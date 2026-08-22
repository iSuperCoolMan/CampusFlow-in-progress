from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import BaseORM
from app.utils.enums import PaymentStatus


class PaymentORM(BaseORM):
    student_uuid: Mapped[UUID] = mapped_column(ForeignKey("students.uuid"))
    amount: Mapped[int] = mapped_column()
    due_date: Mapped[datetime] = mapped_column()
    paid_date: Mapped[datetime] = mapped_column()
    status: Mapped[PaymentStatus] = mapped_column()
    method: Mapped[str] = mapped_column()


class ScholarshipORM(BaseORM):
    student_uuid: Mapped[UUID] = mapped_column(ForeignKey("students.uuid"))
    name: Mapped[str] = mapped_column()
    amount: Mapped[int] = mapped_column()
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()