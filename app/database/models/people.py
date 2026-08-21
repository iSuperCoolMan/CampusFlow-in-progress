from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.auth import UserORM


class PeopleORM(UserORM):
    __abstract__ = True

    uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()

    __mapper_args__ = {
        "polymorphic_identity": "people",
    }


class StudentORM(PeopleORM):
    student_number: Mapped[str] = mapped_column()
    enrollment_year: Mapped[int] = mapped_column()
    program_uuid: Mapped[UUID] = mapped_column(ForeignKey("programs.uuid"))
    advisor_uuid: Mapped[UUID] = mapped_column(ForeignKey("instructors.uuid"))


class InstructorORM(PeopleORM):
    title: Mapped[str] = mapped_column()
    department_uuid: Mapped[UUID] = mapped_column(ForeignKey("departments.uuid"))


class AdminORM(PeopleORM):
    pass


class RegistrarORM(PeopleORM):
    pass


class FinanceManagerORM(PeopleORM):
    pass


class FacilityManagerORM(PeopleORM):
    pass