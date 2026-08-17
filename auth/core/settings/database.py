from dataclasses import dataclass

from auth.core.settings.base import BaseSettings


@dataclass
class DBSettings(BaseSettings):
    DIRECTORY: str


db = DBSettings(DIRECTORY="sqlite:///auth/database/database.db")