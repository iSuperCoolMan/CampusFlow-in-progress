from typing import Literal

from pydantic import BaseModel


class Token(BaseModel):
    token: str
    role: Literal["access", "refresh", "email"]
    type: str = "bearer"