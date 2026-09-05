import re


class Username(str):
    def __new__(cls, value=""):
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", value):
            raise ValueError("Имя пользователя: 3-20 символов, только буквы, цифры и _")

        return super().__new__(cls, str(value))


class Password(str):
    def __new__(cls, value=""):
        if len(value) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")

        return super().__new__(cls, str(value))