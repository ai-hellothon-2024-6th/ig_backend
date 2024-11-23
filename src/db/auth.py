from src.db import engine, SQLModel, Session, Field, select, and_
from src.utils import tools


class AuthTokens(SQLModel, table=True):
    __tablename__ = "AUTH_TOKENS"

    ig_id: str = Field(default=None, primary_key=True)
    token: str
    valid_until: str


SQLModel.metadata.create_all(engine)


def delete_auth_token(ig_id: str):
    with Session(engine) as session:
        auth_token = session.exec(
            select(AuthTokens).where(AuthTokens.ig_id == ig_id)
        ).first()

        if auth_token:
            session.delete(auth_token)  # 삭제 수행
            session.commit()


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


def find_auth_token_valid(ig_id: str):
    with Session(engine) as session:
        statement = select(AuthTokens).where(
            and_(
                AuthTokens.ig_id == ig_id,
                AuthTokens.valid_until > tools.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            )
        )
        return session.exec(statement).first()
