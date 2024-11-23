from fastapi import APIRouter, Response, Depends
from src.models.auth import AuthDTO
from src.models.comment import *
from src.services import comment as service
from src.utils import jwt, responses
from requests.exceptions import HTTPError
from typing import List

router = APIRouter()


@router.post(
    "/reply/recommend",
    response_model=List[ReplyRecommendationDTO],
    tags=["comment"],
    responses={
        403: responses.forbidden,
    },
)
def recommend_reply(
    dto: CommentDTO, limit: int = 3, auth: AuthDTO = Depends(jwt.verify_jwt)
):
    try:
        return [service.recommend_reply(dto, auth) for _ in range(limit)]

    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


@router.put(
    "/reply/recommend",
    status_code=204,
    response_class=Response,
    tags=["comment"],
    responses={
        403: responses.forbidden,
    },
)
def update_recommend_reply(
    dto: ReplyRecommendationDTO,
    auth: AuthDTO = Depends(jwt.verify_jwt),
):
    try:
        service.update_recommend_reply(dto, auth)
        return Response(status_code=204)

    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


@router.post(
    "/reply/{comment_id}",
    status_code=201,
    response_class=Response,
    tags=["comment"],
    responses={
        403: responses.forbidden,
    },
)
def reply_comment(
    comment_id: str,
    dto: ReplyRecommendationDTO,
    auth: AuthDTO = Depends(jwt.verify_jwt),
):
    try:
        service.reply_comment(comment_id, dto.reply, auth.access_token)
        return Response(status_code=201)

    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


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
        other_user_comments, scores = service.get_comments_and_scores(media_id, auth)
        return service.filter_by_score(other_user_comments, scores, lambda x: x >= 0.7)

    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


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
        other_user_comments, scores = service.get_comments_and_scores(media_id, auth)
        filtered_comments = service.filter_by_score(
            other_user_comments, scores, lambda x: x < 0.7, toxicity=True
        )
        return service.update_filtered_text(filtered_comments)

    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)
