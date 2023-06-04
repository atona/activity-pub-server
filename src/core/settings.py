import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    APP_DOMAIN: str = os.environ.get("APP_DOMAIN")
    APP_PORT: str = os.environ.get("APP_PORT")
    APP_PROTOCOL: str = os.environ.get("APP_PROTOCOL")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER", "127.0.0.1")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "postgres")

    def app_base_url(self):
        port_str = f":{self.APP_PORT}" if self.APP_PORT else ""
        return f"{self.APP_PROTOCOL}://{self.APP_DOMAIN}{port_str}"


settings = Settings()
