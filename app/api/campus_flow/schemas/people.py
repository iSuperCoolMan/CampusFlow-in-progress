from uuid import UUID

from app.api.auth.schemas.user import UserCreate


class People(UserCreate):
    first_name: str
    last_name: str


class Student(People):
    student_number: str
    enrollment_year: int
    program_uuid: UUID
    advisor_uuid: UUID


class Instructor(People):
    title: str
    department_uuid: UUID