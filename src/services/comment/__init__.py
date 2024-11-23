import re
from src.models.auth import AuthDTO
from src.models.comment import *
from src.models.alice_ml import ScoreResponseDTO
from src.db import auth as auth_db
from src.db import comment as comment_db
from src.db.comment import UserComment
from src.api.instagram import comment as comment_api
from src.api import alice_ml as ml_api
from src.api import openai as openai_api


def system_message(text: str):
    return {"role": "system", "content": text}


def user_message(text: str):
    return {"role": "user", "content": text}


def filter_my_comments(comments: list[CommentDTO]):
    return list(filter(lambda x: not x.user, comments))


def get_scores_from_comments(comments: list[CommentDTO]):
    return ml_api.get_scores([comment.text for comment in comments])


def filter_by_score(
    comments: list[CommentDTO],
    scores: list[ScoreResponseDTO],
    func: callable,
    toxicity: bool = False,
):
    result: list[CommentDTO] = []
    for i in range(len(comments)):
        if func(scores[i].score):
            comments[i].toxicity = toxicity
            result.append(comments[i])
    return result


def sync_others_comments(media_id: str, auth: AuthDTO):
    auth_tokens = auth_db.find_auth_token_valid(auth.user_id)
    comment_id_list = comment_api.get_comments(media_id, auth_tokens.token)
    saved_comment_ids = comment_db.find_user_comment_ids(auth.user_id)
    # print(comment_id_list)
    # print(saved_comment_ids)
    comments = [
        comment_api.get_comment_detail(comment_id, auth_tokens.token)
        for comment_id in [id for id in comment_id_list if id not in saved_comment_ids]
    ]
    # print(len(comments))
    others_comments = filter_my_comments(comments)
    # print(len(others_comments))
    # scores = get_scores_from_comments(others_comments)
    user_comments = []
    for idx, comment in enumerate(others_comments):
        toxicity = int(
            re.match(
                "\d",
                openai_api.generate_text(
                    [
                        system_message("주어진 인스타 댓글을 분류합니다."),
                        system_message(
                            "욕설, 조롱, 비난, 비판, 악담, 저주, 부정적인 내용을 포함한 댓글은 유해(1), 아닌 경우는 유해하지 않음(0)으로 분류합니다."
                        ),
                        system_message("결과를 숫자로 나타내주세요."),
                        user_message(others_comments[idx].text),
                        system_message("no yapping, 답변만 반환해주세요."),
                    ]
                ),
            ).group()
        )

        user_comments.append(
            UserComment(
                id=comment.id,
                ig_id=auth.user_id,
                media_id=media_id,
                comment_id=comment.id,
                toxicity=bool(toxicity),
                filtered=(
                    ml_api.get_filterd_text(comment.text) if bool(toxicity) else ""
                ),
                text=comment.text,
            )
        )
    for idx, comment in enumerate(user_comments):
        if comment.toxicity:
            comment.category = 0
            continue
        comment.category = int(
            re.match(
                "\d",
                openai_api.generate_text(
                    [
                        system_message("주어진 인스타 댓글을 분류합니다."),
                        system_message("이 댓글은 긍정적인 편인 댓글입니다."),
                        system_message(
                            "Interest, Search형태로 나오는 댓글, 즉 나의 콘텐츠나 상품에 대해 질문하는 사람들의 댓글인 감성적 충성도(1)와\
                           Action Share형태로 나오는 댓글, 즉 사용 경험 설명, 제품 설명, 콘텐츠를 지속적으로 소비한다고 밝힌 사람에 대한 댓글인 행동적 충성도(2)와\
                           그 둘 중에 아무것에도 속하지 않는 댓글인 중립적 충성도(3)를 분류합니다."
                        ),
                        system_message("결과를 숫자로 나타내주세요."),
                        user_message(others_comments[idx].text),
                        system_message("no yapping, 답변만 반환해주세요."),
                    ]
                ),
            ).group()
        )
    comment_db.save_user_comments(user_comments)


def get_others_comment_by_toxicity(media_id: str, auth: AuthDTO, toxicity: bool):
    auth_tokens = auth_db.find_auth_token_valid(auth.user_id)
    comments = comment_db.find_user_comments_by_toxicity(media_id, toxicity)
    result = []
    for comment in comments:
        detail = comment_api.get_comment_detail(comment.id, auth_tokens.token)
        result.append(
            CommentDTO(
                id=comment.id,
                text=detail.text,
                timestamp=detail.timestamp,
                toxicity=comment.toxicity,
                category=comment.category,
                filtered=comment.filtered,
                username=detail.username,
                user=False,
                like_count=detail.like_count,
            )
        )
    return result


def get_recommend_reply(dto: CommentDTO, auth: AuthDTO):
    # auth_tokens = auth_db.find_auth_token_valid(auth.user_id)
    comments = comment_db.find_recommend_comment(auth.user_id, dto.id)
    return comments
