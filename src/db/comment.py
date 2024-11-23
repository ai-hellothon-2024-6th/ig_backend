from src.db import engine, SQLModel, Session, Field, select, and_


class UserComment(SQLModel, table=True):
    __tablename__ = "USER_COMMENTS"

    id: str = Field(default=None, primary_key=True)
    media_id: str
    ig_id: str
    text: str = Field(max_length=2200)
    toxicity: bool  # False: positive, True: negative
    category: int = None  # 0: negative, 1: neutral, 2: emotional, 3: motivational
    filtered: str = ""  # 부정적 댓글에만 포함, 긍정적 댓글은 빈 문자열


class RecommendComment(SQLModel, table=True):
    __tablename__ = "RECOMMEND_COMMENTS"

    id: int = Field(
        default=None,
        primary_key=True,
    )
    ig_id: str
    comment_id: str
    reply: str = Field(max_length=2200)


SQLModel.metadata.create_all(engine)


def update_recommend_comment(recommend_comment: RecommendComment):
    with Session(engine) as session:
        statement = select(RecommendComment).where(
            RecommendComment.id == recommend_comment.id
        )
        existing_comment = session.exec(statement).one_or_none()
        if existing_comment:
            existing_comment.reply = recommend_comment.reply
            session.add(existing_comment)
            session.commit()


def save_recommend_comment(recommend_comment: RecommendComment):
    with Session(engine) as session:
        session.add(recommend_comment)
        session.commit()


def find_recommend_comment(ig_id: str, comment_id: str):
    # print("find")
    with Session(engine) as session:
        statement = select(RecommendComment).where(
            and_(
                RecommendComment.ig_id == ig_id,
                RecommendComment.comment_id == comment_id,
            )
        )
        return session.exec(statement).all()


def save_user_comments(user_comments: list[UserComment]):
    with Session(engine) as session:
        # session.add(user_comment)
        session.add_all(user_comments)
        session.commit()


def find_user_comment_ids(ig_id: str):
    with Session(engine) as session:
        statement = select(UserComment.id).where(UserComment.ig_id == ig_id)
        return set([id for id in session.exec(statement).all()])


def find_user_comments_by_toxicity(media_id: str, toxicity: bool):
    with Session(engine) as session:
        statement = select(UserComment).where(
            and_(
                UserComment.media_id == media_id,
                UserComment.toxicity == toxicity,
            )
        )
        return list(session.exec(statement).all())


def get_comments_by_category(category: str, ig_id: str):
    category_code = 0
    if category == "neutral":
        category_code = 1
    elif category == "emotional":
        category_code = 2
    elif category == "motivational":
        category_code = 3
    with Session(engine) as session:
        statement = select(UserComment).where(
            and_(
                UserComment.ig_id == ig_id,
                UserComment.category == category_code,
            )
        )
        return list(session.exec(statement).all())
