import re
from abc import ABC, abstractmethod
from typing import Annotated

from pydantic import AfterValidator


class Validator(ABC, str):
    @staticmethod
    @abstractmethod
    def validate(value):
        pass


class UsernameValidator(Validator):
    @staticmethod
    def validate(value):
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", value):
            raise ValueError("Имя пользователя: 3-20 символов, только буквы, цифры и _")

        return value


class PasswordValidator(Validator):
    @staticmethod
    def validate(value):
        if len(value) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")

        return value


UsernameStr = Annotated[str, AfterValidator(UsernameValidator.validate)]
PasswordStr = Annotated[str, AfterValidator(PasswordValidator.validate)]