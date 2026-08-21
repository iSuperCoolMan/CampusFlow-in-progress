import importlib
import os

from dataclasses import dataclass, field

from fastapi_sso import __all__ as sso_methods_names, SSOBase

from .base import BaseSettings
from .uris import uris


@dataclass
class SSOData:
    name: str
    method: SSOBase
    params: dict | None


@dataclass
class SSOSettings(BaseSettings):
    __sso_methods: dict[str: SSOData] = field(default_factory=dict)

    def __post_init__(self):
        not_working_sso_names = []

        for sso_class_name in sso_methods_names:
            sso_method = self.__create_sso_method(sso_class_name)

            if sso_method:
                self.__sso_methods[sso_method.name] = sso_method
            else:
                not_working_sso_names.append(sso_class_name)

        if not_working_sso_names:
            print(
                f" - {", ".join(not_working_sso_names)}\n"
                f" - sso not setting up."
            )

        if not_working_sso_names and self.__sso_methods:
            print(" - ------------------")

        if self.__sso_methods:
            print(
                f" - {", ".join(self.__sso_methods.keys())}\n"
                f" - sso setting up."
            )


    def __create_sso_method(self, class_name: str) -> SSOData | None:
        if not class_name.endswith("SSO"):
            return None

        name = class_name[:-3]
        name_lower = name.lower()
        name_upper = name.upper()

        module = importlib.import_module(f"fastapi_sso.sso.{name_lower}")
        sso_class = getattr(module, class_name)

        id_path = f"{name_upper}_CLIENT_ID"
        secret_path = f"{name_upper}_CLIENT_SECRET"

        try:
            method = sso_class(
                client_id=os.environ[id_path],
                client_secret=os.environ[secret_path],
                redirect_uri=f"{uris.BASE_URI}auth/sso/callback/{name_lower}",
                allow_insecure_http=True
            )
        except KeyError:
            return None

        if name_lower == "google":
            params = {"prompt": "consent", "access_type": "offline"}
        else:
            params = None

        return SSOData(
            name=name_lower,
            method=method,
            params=params
        )

    def get_sso_data_by_name(self, name: str) -> SSOData:
        if self.__sso_methods.keys().__contains__(name):
            return self.__sso_methods[name]
        else:
            raise ValueError


sso = SSOSettings()
