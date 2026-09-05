from dataclasses import dataclass

from .base import BaseSettings


@dataclass
class DBSettings(BaseSettings):
    DIRECTORY: str


db = DBSettings(DIRECTORY="sqlite+aiosqlite:///app/database/database.db")