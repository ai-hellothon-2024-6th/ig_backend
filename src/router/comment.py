from fastapi import APIRouter, Response, Depends
from src.models.auth import AuthDTO
from src.models.comment import CommentDTO
from src.models.alice_ml import ScoreResponseDTO
from src.api.instagram import comment as comment_api
from src.api import alice_ml as ml_api
from src.utils import jwt, responses
from requests.exceptions import HTTPError
from typing import List

router = APIRouter()


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


@router.get(
    "/{media_id}/positive",
    response_model=List[CommentDTO],
    tags=["comment"],
    responses={
        403: responses.forbidden,
    },
)
def positive_comments(media_id: str, auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        other_user_comments, scores = get_comments_and_scores(media_id, auth)
        return filter_by_score(other_user_comments, scores, lambda x: x >= 0.7)

    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )


@router.get(
    "/{media_id}/negative",
    response_model=List[CommentDTO],
    tags=["comment"],
    responses={
        403: responses.forbidden,
    },
)
def negative_comments(media_id: str, auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        other_user_comments, scores = get_comments_and_scores(media_id, auth)
        filtered_comments = filter_by_score(
            other_user_comments, scores, lambda x: x < 0.7, toxicity=True
        )
        for comment in filtered_comments:
            comment.filtered = ml_api.get_filterd_text(comment.text)
        return filtered_comments

    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )
