from datetime import datetime
from typing import Literal, Annotated, Any
from uuid import UUID

from annotated_types import Interval

from app.api.campus_flow.schemas.base import BaseModelWithUUID


class Course(BaseModelWithUUID):
    title: str
    department_uuid: UUID
    code: str
    credits: str
    description: str


class CourseOffering(BaseModelWithUUID):
    course_uuid: UUID
    program_uuid: UUID
    term: Literal["Fall", "Spring", "Summer"]
    year: int
    instructor_uuid: UUID
    room_uuid: UUID


class Section(BaseModelWithUUID):
    offering_uuid: UUID
    section_number: int
    capacity: int
    schedule: dict[str, Any]
    days_of_week: Annotated[int, Interval(ge=1, le=7)]


class Enrollments(BaseModelWithUUID):
    student_uuid: UUID
    section_uuid: UUID
    status: Literal["enrolled", "withdrawn"]
    enrolled_on: datetime
    grade_uuid: UUID


class Grade(BaseModelWithUUID):
    enrollment_uuid: UUID
    value: Annotated[int, Interval(ge=1, le=5)]
    date_recorded: datetime