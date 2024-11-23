from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IG_CLIENT_ID: str
    IG_CLIENT_SECRET: str
    IG_GRANT_TYPE: str = "authorization_code"
    JWT_SECRET_KEY: str
    ALICE_ML_API_KEY: str
    DB_ENGINE: str = "mysql+pymysql"
    DB_HOST: str  # 주소
    DB_PORT: int  # 포트
    DB_NAME: str  # 데이터베이스 이름
    DB_USER: str  # 사용자 이름
    DB_PASSWORD: str  # 비밀번호

    class Config:
        env_file = ".env"


settings = Settings()
