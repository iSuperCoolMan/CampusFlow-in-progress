from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models import BaseORM


class ProfileORM(BaseORM):
    __abstract__ = True

    uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()


class StudentORM(ProfileORM):
    student_number: Mapped[str] = mapped_column()
    enrollment_year: Mapped[int] = mapped_column()
    program_uuid: Mapped[UUID] = mapped_column(ForeignKey("programs.uuid"))
    advisor_uuid: Mapped[UUID] = mapped_column(ForeignKey("instructors.uuid"))


class InstructorORM(ProfileORM):
    title: Mapped[str] = mapped_column()
    department_uuid: Mapped[UUID] = mapped_column(ForeignKey("departments.uuid"))


class AdminORM(ProfileORM):
    pass


class RegistrarORM(ProfileORM):
    pass


class FinanceManagerORM(ProfileORM):
    pass


class FacilityManagerORM(ProfileORM):
    pass