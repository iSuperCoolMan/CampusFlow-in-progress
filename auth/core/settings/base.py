from dataclasses import dataclass


class BaseSettings:
    def __post_init__(self):
        kwargs = self.__dict__
        null_kwargs = []

        for key in kwargs:
            if not kwargs[key]:
                null_kwargs.append(key)

        if null_kwargs:
            raise ValueError(f"{null_kwargs} cannot be null.")


@dataclass
class TokenSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int