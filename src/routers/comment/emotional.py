from fastapi import APIRouter, Response, Depends
from src.models.auth import AuthDTO
from src.models.comment import *
from src.services import comment as comment_service
from src.services.comment import loyalty as loyalty_service
from src.utils import jwt, responses
from requests.exceptions import HTTPError
from typing import List

router = APIRouter()


@router.get(
    "",
    response_model=List[PositiveCommentDTO],
    tags=["emotional"],
    responses={
        403: responses.forbidden,
    },
)
def emotional_comments(auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        return loyalty_service.get_comments_by_category(
            PositiveCommentCategory.EMOTIONAL,
            auth,
        )
    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


@router.get(
    "/summary",
    response_model=CommentSummaryDTO,
    tags=["emotional"],
    responses={
        403: responses.forbidden,
    },
)
def emotional_comments_summary(auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        return loyalty_service.get_summary_by_category(
            PositiveCommentCategory.EMOTIONAL,
            auth,
        )
    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


@router.get(
    "/insight",
    response_model=List[CommentInsightDTO],
    tags=["emotional"],
    responses={
        403: responses.forbidden,
    },
)
def emotional_comments_insights(
    limit: int = 3,
    auth: AuthDTO = Depends(jwt.verify_jwt),
):
    try:
        return [
            loyalty_service.get_insights_by_category(
                PositiveCommentCategory.EMOTIONAL,
                auth,
            )
            for _ in range(limit)
        ]

    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )
