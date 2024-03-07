from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve()


class Settings(BaseSettings):
    postgres_username: str
    postgres_password: str
    postgres_hostname: str
    postgres_port: str
    postgres_name: str

    class Config:
        env_file = "../.env"


settings = Settings()
