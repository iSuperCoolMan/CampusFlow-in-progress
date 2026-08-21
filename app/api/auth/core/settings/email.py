from dataclasses import dataclass

from .base import BaseSettings, TokenSettings, EnvField


@dataclass
class EmailSettings(BaseSettings):
    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str


email = EmailSettings(
    HOST = EnvField("EMAIL_HOST"),
    PORT = EnvField("EMAIL_PORT"),
    USERNAME = EnvField("EMAIL_USERNAME"),
    PASSWORD = EnvField("EMAIL_PASSWORD")
)

email_token = TokenSettings(
    SECRET_KEY=EnvField("EMAIL_TOKEN_SECRET_KEY"),
    ALGORITHM=EnvField("EMAIL_TOKEN_ALGORITHM"),
    EXPIRE_MINUTES=20
)