from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True


class DBSettings(BaseSettings):
    PGUSER: str
    PGPASSWORD: str
    PGHOST: str
    PGPORT: str = "5432"
    PGDATABASE: str

    class Config:
        case_sensitive = True


settings = Settings()  # type: ignore
db_settings = DBSettings()  # type: ignore
SQLALCHEMY_DATABASE_URI = \
    f"postgresql://{db_settings.PGUSER}:{db_settings.PGPASSWORD}@{db_settings.PGHOST}:{db_settings.PGPORT}/{db_settings.PGDATABASE}"
