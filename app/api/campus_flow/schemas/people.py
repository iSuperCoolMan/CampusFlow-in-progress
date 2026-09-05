from typing import Union, Annotated
from uuid import UUID

from pydantic import BaseModel, Field, RootModel

from app.utils.enums import Role


class People(BaseModel):
    role: Role
    first_name: str
    last_name: str


class Student(People):
    role = Role.student
    student_number: str
    enrollment_year: int
    program_uuid: UUID
    advisor_uuid: UUID


class Instructor(People):
    role = Role.instructor
    title: str
    department_uuid: UUID


class Admin(People):
    role = Role.admin


class Registrar(People):
    role = Role.registrar


class FinanceManager(People):
    role = Role.finance_manager


class FacilityManager(People):
    role = Role.facility_manager


PeopleUnion = Union[Student, Instructor, Admin, Registrar, FinanceManager, FacilityManager]
PeoplePayload = RootModel[Annotated[PeopleUnion, Field(discriminator="role")]]