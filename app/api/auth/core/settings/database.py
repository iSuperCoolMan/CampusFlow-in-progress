from dataclasses import dataclass

from .base import BaseSettings


@dataclass
class DBSettings(BaseSettings):
    DIRECTORY: str


db = DBSettings(DIRECTORY="sqlite:///app/database/database.db")