from sqlmodel import (
    create_engine,
    Session,
    SQLModel,
    Field,
    select,
    and_,
)
from src.settings import settings

DB_ENGINE = settings.DB_ENGINE
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD

DATABASE_URL = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
