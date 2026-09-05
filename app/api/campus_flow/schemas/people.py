from uuid import UUID

from pydantic import BaseModel


class People(BaseModel):
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