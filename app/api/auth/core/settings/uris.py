from dataclasses import dataclass

from .base import BaseSettings


@dataclass
class URISettings(BaseSettings):
    BASE_URI: str


uris = URISettings(BASE_URI="http://localhost:8000/api/v1")