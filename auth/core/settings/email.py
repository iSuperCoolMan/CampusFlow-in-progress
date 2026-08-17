import os
from dataclasses import dataclass

from auth.core.settings.base import BaseSettings, TokenSettings


@dataclass
class EmailSettings(BaseSettings):
    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str


email = EmailSettings(
    HOST = os.getenv("EMAIL_HOST"),
    PORT = os.getenv("EMAIL_PORT"),
    USERNAME = os.getenv("EMAIL_USERNAME"),
    PASSWORD = os.getenv("EMAIL_PASSWORD")
)

email_token = TokenSettings(
    SECRET_KEY=os.getenv("EMAIL_TOKEN_SECRET_KEY"),
    ALGORITHM=os.getenv("EMAIL_TOKEN_ALGORITHM"),
    EXPIRE_MINUTES=20
)