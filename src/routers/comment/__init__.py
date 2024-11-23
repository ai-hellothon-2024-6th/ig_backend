from typing import List
from fastapi import APIRouter, Response, Depends
from requests.exceptions import HTTPError
from src.models.auth import AuthDTO
from src.models.comment import *
from src.services import comment as comment_service
from src.services.comment import reply as reply_service
from src.utils import jwt, responses

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
        saved_recommend_reply = comment_service.get_recommend_reply(dto, auth)
        print(saved_recommend_reply)
        if len(saved_recommend_reply) > limit:
            return [
                ReplyRecommendationDTO(id=f"{r.id}", reply=r.reply)
                for r in saved_recommend_reply[:limit]
            ]
        for _ in range(limit):
            reply_service.recommend_reply(dto, auth)
        return [
            ReplyRecommendationDTO(id=f"{r.id}", reply=r.reply)
            for r in comment_service.get_recommend_reply(dto, auth)
        ]

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
        comment_service.update_recommend_reply(dto, auth)
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
        comment_service.reply_comment(comment_id, dto.reply, auth.access_token)
        return Response(status_code=201)

    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )


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
        comment_service.sync_others_comments(media_id, auth)
        return comment_service.get_others_comment_by_toxicity(media_id, auth, False)

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
        comment_service.sync_others_comments(media_id, auth)
        return comment_service.get_others_comment_by_toxicity(media_id, auth, True)

    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)
