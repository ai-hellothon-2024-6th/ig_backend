from typing import List
from src.models.auth import AuthDTO
from src.models.comment import *
from src.models.alice_ml import ScoreResponseDTO
from src.api.instagram import comment as comment_api
from src.api import alice_ml as ml_api
from faker import Faker  # TODO : 테스트용 코드, 추후 삭제
import datetime  # TODO : 테스트용 코드, 추후 삭제
import random  # TODO : 테스트용 코드, 추후 삭제

fake = Faker("en_US")


def system_message(text: str):
    return {
        "role": "system",
        "content": text,
    }


def user_message(text: str):
    return {
        "role": "user",
        "content": text,
    }


def get_comments_by_category(category: str, auth: AuthDTO) -> List[PositiveCommentDTO]:
    # TODO : DB 호출로 전환
    comments = []
    prompt = ""
    if category == PositiveCommentCategory.EMOTIONAL:
        prompt += "Interest, Search 형태로 나오는 댓글, 즉 나의 콘텐츠나 상품에 대해 질문하는 사람들의 댓글을 줄글로 자연스럽게 작성합니다."
    if category == PositiveCommentCategory.MOTIVATIONAL:
        prompt += "Action Share 형태로 나오는 댓글 즉 사용 경험 설명, 제품 설명, 콘텐츠를 지속적으로 소비한다고 밝힌 사람에 대한 댓글을 줄글로 자연스럽게 작성합니다."
    for i in range(5):
        comments.append(
            PositiveCommentDTO(
                id=f"{random.randint(1, 1000000)}",
                text=ml_api.get_generative_text(
                    [
                        system_message(
                            "주어진 내용에 맞춰 임의의 길이의 인스타 스타일의 댓글을 생성합니다."
                        ),
                        user_message(prompt),
                        system_message("no yapping, 답변만 반환해주세요."),
                    ]
                ),
                timestamp=fake.date_time_this_month(
                    before_now=True, tzinfo=datetime.timezone.utc
                ).isoformat(timespec="seconds"),
                username=fake.user_name().lower(),
                category=category,
            ),
        )
    return comments


def recommend_reply(dto: CommentDTO, auth: AuthDTO):
    # TODO : auth를 통한 유저 확인 후 말투 RAG
    text = ""
    text += (
        "이 댓글은 부정적으로 분류되었습니다.\n"
        if dto.toxicity
        else "이 댓글은 부정적이지 않다고 분류되었습니다.\n"
    )
    text += f"{dto.text}\n"
    response = ml_api.get_generative_text(
        [
            system_message("주어진 내용에 맞춰 인스타 답변 리플을 생성합니다."),
            user_message(text),
            system_message("no yapping, 답변만 반환해주세요."),
        ]
    )
    return ReplyRecommendationDTO(reply=response)


def filter_my_comments(comments: List[CommentDTO]):
    return list(filter(lambda x: not x.user, comments))


def get_scores_from_comments(comments: List[CommentDTO]):
    return ml_api.get_scores([comment.text for comment in comments])


def filter_by_score(
    comments: List[CommentDTO],
    scores: List[ScoreResponseDTO],
    func: callable,
    toxicity: bool = False,
):
    result: List[CommentDTO] = []
    for i in range(len(comments)):
        if func(scores[i].score):
            comments[i].toxicity = toxicity
            result.append(comments[i])
    return result


def get_comments_and_scores(media_id: str, auth: AuthDTO):
    # TODO : DB 호출로 전환
    comment_id_list = comment_api.get_comments(media_id, auth.access_token)
    comments = [
        comment_api.get_comment_detail(comment, auth.access_token)
        for comment in comment_id_list
    ]
    other_user_comments = filter_my_comments(comments)
    scores = get_scores_from_comments(other_user_comments)
    return other_user_comments, scores


def update_filtered_text(filtered_comments: List[CommentDTO]):
    for comment in filtered_comments:
        comment.filtered = ml_api.get_filterd_text(comment.text)
    return filtered_comments
