from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IG_CLIENT_ID: str
    IG_CLIENT_SECRET: str
    IG_GRANT_TYPE: str = "authorization_code"
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
