import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_domain: str = os.environ.get("APP_DOMAIN", "127.0.0.1")
    app_port: str = os.environ.get("APP_PORT", "8000")
    app_protocol: str = os.environ.get("APP_PROTOCOL", "http")

    def get_base_url(self):
        port_str = f":{self.app_port}" if self.app_port else ""
        return f"{self.app_protocol}:{self.app_domain}{port_str}"


def get_settings():
    return Settings()
