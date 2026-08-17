from dataclasses import dataclass

from auth.core.settings.base import BaseSettings


@dataclass
class URISettings(BaseSettings):
    BASE_URI: str


uris = URISettings(BASE_URI="http://localhost:8000/auth/v1")