from .base import TokenSettings, EnvField

access_token = TokenSettings(
    SECRET_KEY=EnvField("ACCESS_TOKEN_SECRET_KEY"),
    ALGORITHM=EnvField("ACCESS_TOKEN_ALGORITHM"),
    EXPIRE_MINUTES=30
)

refresh_token = TokenSettings(
    SECRET_KEY=EnvField("REFRESH_TOKEN_SECRET_KEY"),
    ALGORITHM=EnvField("REFRESH_TOKEN_ALGORITHM"),
    EXPIRE_MINUTES=7*1440
)