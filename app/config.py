# Reference Link -> https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()


# from typing import Any, Callable, Set

# from pydantic import (
#     AliasChoices,
#     AmqpDsn,
#     BaseModel,
#     Field,
#     ImportString,
#     PostgresDsn,
#     RedisDsn,
# )