from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    pg_dsn: str = Field(alias="PG_DSN")
    project_id: int = Field(alias="PROJECT_ID")
