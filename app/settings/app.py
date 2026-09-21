from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict()

    mqtt_host: str = Field()
    mqtt_port: int = Field(default=1883)
