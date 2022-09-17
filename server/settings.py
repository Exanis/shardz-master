"""
Settings holder for the app
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings holder"""

    debug: bool = False
    identification_url: str = "http://identification/"
    servers_url: str = "http://servers/"
    api_key: str = "invalid_key"


settings = Settings()
