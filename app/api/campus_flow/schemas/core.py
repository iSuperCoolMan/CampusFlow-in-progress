from datetime import datetime
from typing import Literal, Annotated
from uuid import UUID

from annotated_types import Interval, Timezone

from app.api.campus_flow.schemas.base import BaseModelWithUUID


class University(BaseModelWithUUID):
    name: str
    country: str
    established_year: Annotated[int, Interval(ge=0, le=datetime.now().year)]


class Campus(BaseModelWithUUID):
    name: str
    university_uuid: UUID
    location: str
    timezone: Timezone


class Department(BaseModelWithUUID):
    name: str
    campus_uuid: UUID
    code: str


class Program(BaseModelWithUUID):
    name: str
    department_uuid: UUID
    code: str
    level: Literal["Bachelor", "Master", "PhD"]
    duration_years: int