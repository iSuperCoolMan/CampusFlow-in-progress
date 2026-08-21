from uuid import UUID

from pydantic import BaseModel


class BaseModelWithUUID(BaseModel):
    uuid: UUID