import os

from dataclasses import dataclass, fields
from typing import Any


class EnvField:
    def __init__(self, env_name: str):
        self.env_name = env_name

    def get_value(self) -> Any:
        return os.getenv(self.env_name)


@dataclass
class BaseSettings:
    def __post_init__(self):
        null_names = []
        null_env_names = []

        for field_def in fields(self):
            field_name = field_def.name
            current_value = getattr(self, field_name)

            if isinstance(current_value, EnvField):
                env_name = current_value.env_name
                resolved_value = current_value.get_value()

                setattr(self, field_name, resolved_value)

                if not resolved_value:
                    null_names.append(field_name)
                    null_env_names.append(env_name)
            elif not current_value:
                null_names.append(field_name)

        if null_names:
            error_message = f"In {self.__class__.__name__} {null_names} cannot be null."

            if null_env_names:
                error_message += f"\nCheck env variables: {null_env_names}"

            raise ValueError(error_message)


@dataclass
class TokenSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int