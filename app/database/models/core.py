from uuid import UUID

from annotated_types import Timezone
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import BaseORM
from app.utils.annotations import established_year_annotation
from app.utils.enums import ProgramLevel


class UniversityORM(BaseORM):
    name: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    established_year: Mapped[established_year_annotation] = mapped_column()


class CampusORM(BaseORM):
    name: Mapped[str] = mapped_column()
    university_uuid: Mapped[UUID] = mapped_column(ForeignKey("universities.uuid"))
    location: Mapped[str] = mapped_column()
    timezone: Mapped[Timezone] = mapped_column(String())


class DepartmentORM(BaseORM):
    name: Mapped[str] = mapped_column()
    campus_uuid: Mapped[UUID] = mapped_column(ForeignKey("campuses.uuid"))
    code: Mapped[str] = mapped_column()


class ProgramORM(BaseORM):
    name: Mapped[str] = mapped_column()
    department_uuid: Mapped[UUID] = mapped_column(ForeignKey("departments.uuid"))
    code: Mapped[str] = mapped_column()
    level: Mapped[ProgramLevel] = mapped_column()
    duration_years: Mapped[int] = mapped_column()