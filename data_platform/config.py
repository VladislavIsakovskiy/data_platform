from pydantic import computed_field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppSettings(BaseSettings):
    HOST: str
    PORT: int
    LOG_LEVEL: str = "INFO"
    LOG_FOLDER: str = "/logs"

    model_config = SettingsConfigDict(env_prefix="APP_")

class DBSettings(BaseSettings):
    URL: str
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    model_config = SettingsConfigDict(env_prefix="DB_")

class BrokerSettings(BaseSettings):
    HOST: str
    PORT: int
    TOPIC: str

    @computed_field
    @property
    def url(self) -> str:
        return f"{self.HOST}:{self.PORT}"

    model_config = SettingsConfigDict(env_prefix="KAFKA_")


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    broker: BrokerSettings = BrokerSettings()

settings = Settings()
