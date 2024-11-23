import datetime
from src.models.comment import *
from src.models.auth import AuthDTO
from src.utils import dt_format
from src.api import ml as ml_api
from src.services.comment import system_message, user_message


def get_summary_by_category(category: str, auth: AuthDTO) -> CommentSummaryDTO:
    prompt = ""
    if category == PositiveCommentCategory.EMOTIONAL:
        prompt += "Interest, Search 형태로 나오는 댓글, 즉 나의 콘텐츠나 상품에 대해 질문하는 사람들의 댓글을 줄글로 자연스럽게 작성합니다."
    if category == PositiveCommentCategory.MOTIVATIONAL:
        prompt += "Action Share 형태로 나오는 댓글 즉 사용 경험 설명, 제품 설명, 콘텐츠를 지속적으로 소비한다고 밝힌 사람에 대한 댓글을 줄글로 자연스럽게 작성합니다."
    summary = ml_api.get_generative_text(
        [
            system_message("주어진 내용에 맞춰 인스타그램의 댓글 요약을 생성합니다."),
            user_message("이 글은 200~300자 사이에 3줄로 요약된 글입니다."),
            user_message(prompt),
            system_message("no yapping, 줄글만 반환해주세요."),
        ]
    )
    return CommentSummaryDTO(
        text=summary,
        timestamp=dt_format(datetime.datetime.now()),
    )


def get_insights_by_category(category: str, auth: AuthDTO) -> CommentInsightDTO:
    prompt = ""
    if category == PositiveCommentCategory.EMOTIONAL:
        prompt += "Interest, Search 형태의 관심사, 즉 나의 콘텐츠나 상품에 대해 질문하는 사람들에 대한 인사이트를 제안합니다."
    if category == PositiveCommentCategory.MOTIVATIONAL:
        prompt += "Action Share 형태의 관심사, 즉 사용 경험 설명, 제품 설명, 콘텐츠를 지속적으로 소비한다고 밝힌 사람에 대한 인사이트를 제안합니다."
    summary = ml_api.get_generative_text(
        [
            system_message(
                "주어진 내용에 맞춰 마케팅 방식 또는 행동 방식 등을 추천하는 글을 생성합니다."
            ),
            user_message("이 글은 150자 이내로 작성되어야 합니다."),
            user_message(prompt),
            system_message("no yapping, 줄글만 반환해주세요."),
        ]
    )
    return CommentInsightDTO(
        text=summary,
        timestamp=dt_format(datetime.datetime.now()),
    )


def get_comments_by_category(category: str, auth: AuthDTO) -> list[PositiveCommentDTO]:

    return comments
