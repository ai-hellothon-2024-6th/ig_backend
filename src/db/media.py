from src.db import engine, SQLModel, Session, Field, select, and_
from src.models.media import MediaDTO


class UserMedia(SQLModel, table=True):
    __tablename__ = "USER_MEDIA"

    id: str = Field(default=None, primary_key=True)
    ig_id: str
    caption: str = Field(sa_column_kwargs={"length": 2200})


def save_user_media(user_media: list[MediaDTO], user_id: str):
    with Session(engine) as session:
        for user_media in user_media:
            session.merge(
                UserMedia(id=user_media.id, ig_id=user_id, caption=user_media.caption)
            )
        session.commit()


def find_all_user_media(ig_id: str):
    with Session(engine) as session:
        statement = select(UserMedia).where(UserMedia.ig_id == ig_id)
        return session.exec(statement).all()


SQLModel.metadata.create_all(engine)
