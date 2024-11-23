from src.db import engine, SQLModel, Session, Field, select, and_
from src.utils import tools
import datetime


class AuthTokens(SQLModel, table=True):
    __tablename__ = "AUTH_TOKENS"

    ig_id: str = Field(default=None, primary_key=True)
    token: str
    valid_until: str


def save_auth_token(ig_id: str, token: str, valid_until: str):
    with Session(engine) as session:
        new_auth_token = AuthTokens(
            ig_id=ig_id,
            token=token,
            valid_until=valid_until,
        )
        # session.add(new_auth_token)
        session.merge(new_auth_token)  # Upsert
        session.commit()


def find_auth_token(ig_id: str):
    with Session(engine) as session:
        statement = select(AuthTokens).where(
            and_(
                AuthTokens.ig_id == ig_id,
                AuthTokens.valid_until > tools.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            )
        )
        return session.exec(statement).first()


SQLModel.metadata.create_all(engine)
