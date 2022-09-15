from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = False

    api_key: str = "invalid_key"

    class Config:
        env_file = ".env"


settings = Settings()
