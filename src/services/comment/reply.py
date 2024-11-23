from src.models.comment import *
from src.models.auth import AuthDTO
from src.api import alice_ml as ml_api
from src.api import openai as openai_api
from src.api.instagram import comment as comment_api
from src.services.comment import system_message, user_message
from src.db import media as media_db
from src.db import comment as comment_db
from src.db.comment import RecommendComment
from src.db import auth as auth_db


def recommend_reply(dto: CommentDTO, auth: AuthDTO):
    tone = ";".join([el.caption for el in media_db.find_all_user_media(auth.user_id)])
    text = ""
    text += (
        "이 댓글은 부정적으로 분류되었습니다.\n"
        if dto.toxicity
        else "이 댓글은 부정적이지 않다고 분류되었습니다.\n"
    )
    text += f"{dto.text}\n"
    # response = ml_api.get_generative_text(
    response = openai_api.generate_text(
        [
            system_message("주어진 내용에 맞춰 인스타 답변 리플을 생성합니다."),
            user_message(f"이 글은 이 톤과 유사해야 합니다. : {tone}"),
            user_message(text),
            system_message("no yapping, 답변만 반환해주세요."),
        ]
    )
    dto = RecommendComment(
        ig_id=auth.user_id,
        comment_id=dto.id,
        reply=response,
    )
    comment_db.save_recommend_comment(dto)


def post_reply_comment(comment_id: str, reply: str, user_id: str):
    access_token = auth_db.find_auth_token_valid(user_id).token
    comment_api.post_comment_reply(
        comment_id,
        reply,
        access_token,
    )


def update_recommend_reply(dto: RecommendComment, auth: AuthDTO):
    comment_db.update_recommend_comment(
        RecommendComment(
            id=dto.id,
            reply=dto.reply,
            ig_id=auth.user_id,
            comment_id=dto.comment_id,
        )
    )
