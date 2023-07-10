import os


# TODO: pydantic.BaseSettingsを継承する
class Settings:
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


settings = Settings()
