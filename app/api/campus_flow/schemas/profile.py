from abc import ABC
from typing import Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from fastapi import HTTPException, Body

from app.utils.enums import RoleStr


class Profile(ABC, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID = None
    first_name: str
    last_name: str


    def prepare_to_orm_model(self, user_uuid: UUID):
        self.uuid = user_uuid


class Student(Profile):
    student_number: int
    enrollment_year: int
    program_uuid: UUID
    advisor_uuid: UUID


class Instructor(Profile):
    title: str
    department_uuid: UUID


class Admin(Profile):
    pass


class Registrar(Profile):
    pass


class FinanceManager(Profile):
    pass


class FacilityManager(Profile):
    pass


ProfileUnion = Union[Student, Instructor, Admin, Registrar, FinanceManager, FacilityManager]

profile_model_map = {
    RoleStr.student: Student,
    RoleStr.instructor: Instructor,
    RoleStr.admin: Admin,
    RoleStr.registrar: Registrar,
    RoleStr.finance_manager: FinanceManager,
    RoleStr.facility_manager: FacilityManager,
}


async def validate_profile_payload(role: RoleStr, body: dict = Body(...)) -> Profile:
    profile_model = profile_model_map.get(role)

    if profile_model is None:
        raise HTTPException(status_code=400, detail="Unsupported role")

    try:
        return profile_model(**body)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {e}")