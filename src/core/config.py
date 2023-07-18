from typing import Union

from pydantic import BaseSettings, validator, AnyUrl, AnyHttpUrl


class Settings(BaseSettings):
    CORS_ALLOWED_ORIGINS: Union[str, list[AnyHttpUrl]]

    # POSTGRESQL DEFAULT DATABASE
    DB_HOST: str
    DB_USER: str
    DB_PASSWD: str
    DB_PORT: str = 5432
    DB_NAME: str
    DB_URI: str = ''

    @validator("CORS_ALLOWED_ORIGINS")
    def _assemble_cors_origins(cls, cors_origins: Union[str, list[AnyHttpUrl]]):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    @validator("DB_URI")
    def _assemble_default_db_connection(cls, v: str, values: dict[str, str]) -> str:
        return AnyUrl.build(
            scheme="postgresql+asyncpg",
            user=values["DB_USER"],
            password=values["DB_PASSWD"],
            host=values["DB_HOST"],
            port=values["DB_PORT"],
            path=f"/{values['DB_NAME']}",
        )

    class Config:
        case_sensitive = True


settings: Settings = Settings()
