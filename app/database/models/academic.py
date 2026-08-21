from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseORM
from app.utils.annotations import days_of_week_annotation, grade_value
from app.utils.enums import Term, EnrollmentStatus


class CourseORM(BaseORM):
    title: Mapped[str] = mapped_column()
    department_uuid: Mapped[UUID] = mapped_column(ForeignKey("departments.uuid"))
    code: Mapped[str] = mapped_column()
    credits: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()


class CourseOfferingORM(BaseORM):
    course_uuid: Mapped[UUID] = mapped_column(ForeignKey("courses.uuid"))
    program_uuid: Mapped[UUID] = mapped_column(ForeignKey("programs.uuid"))
    term: Mapped[Term] = mapped_column()
    year: Mapped[int] = mapped_column()
    instructor_uuid: Mapped[UUID] = mapped_column(ForeignKey("instructors.uuid"))
    room_uuid: Mapped[UUID] = mapped_column(ForeignKey("rooms.uuid"))


class SectionORM(BaseORM):
    offering_uuid: Mapped[UUID] = mapped_column(ForeignKey("course_offerings.uuid"))
    section_number: Mapped[int] = mapped_column()
    capacity: Mapped[int] = mapped_column()
    schedule: Mapped[dict[str, Any]] = mapped_column(JSON)
    days_of_week: Mapped[days_of_week_annotation] = mapped_column()


class EnrollmentsORM(BaseORM):
    student_uuid: Mapped[UUID] = mapped_column(ForeignKey("students.uuid"))
    section_uuid: Mapped[UUID] = mapped_column(ForeignKey("sections.uuid"))
    status: Mapped[EnrollmentStatus] = mapped_column()
    enrolled_on: Mapped[datetime] = mapped_column()
    grade_uuid: Mapped[UUID] = mapped_column(ForeignKey("grades.uuid"))


class GradeORM(BaseORM):
    enrollment_uuid: Mapped[UUID] = mapped_column(ForeignKey("enrollments.uuid"))
    value: Mapped[grade_value] = mapped_column()
    date_recorded: Mapped[datetime] = mapped_column()