import os

from auth.core.settings.base import TokenSettings


access_token = TokenSettings(
    SECRET_KEY=os.getenv("ACCESS_TOKEN_SECRET_KEY"),
    ALGORITHM=os.getenv("ACCESS_TOKEN_ALGORITHM"),
    EXPIRE_MINUTES=30
)

refresh_token = TokenSettings(
    SECRET_KEY=os.getenv("REFRESH_TOKEN_SECRET_KEY"),
    ALGORITHM=os.getenv("REFRESH_TOKEN_ALGORITHM"),
    EXPIRE_MINUTES=7*1440
)