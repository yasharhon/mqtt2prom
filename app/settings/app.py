from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # Seems to be necessary to ignore here in order for topics list to be correctly parsed
    model_config = SettingsConfigDict(extra="ignore")

    mqtt_host: str = Field()
    mqtt_port: int = Field(default=1883)
    mqtt_topics: list[str] = Field()
