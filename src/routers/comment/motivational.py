from fastapi import APIRouter, Response, Depends
from src.models.auth import AuthDTO
from src.models.comment import *
from src.services import comment as comment_service
from src.utils import jwt, responses
from requests.exceptions import HTTPError
from typing import List

router = APIRouter()


@router.get(
    "",
    response_model=List[PositiveCommentDTO],
    tags=["motivational"],
    responses={
        403: responses.forbidden,
    },
)
def motivational_comments(auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        return comment_service.get_comments_by_category(
            PositiveCommentCategory.MOTIVATIONAL,
            auth,
        )
    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


@router.get(
    "/summary",
    response_model=CommentSummaryDTO,
    tags=["motivational"],
    responses={
        403: responses.forbidden,
    },
)
def motivational_comments_summary(auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        return comment_service.get_summary_by_category(
            PositiveCommentCategory.MOTIVATIONAL,
            auth,
        )

    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


@router.get(
    "/insight",
    response_model=List[CommentInsightDTO],
    tags=["motivational"],
    responses={
        403: responses.forbidden,
    },
)
def motivational_comments_insights(
    limit: int = 3,
    auth: AuthDTO = Depends(jwt.verify_jwt),
):
    try:
        return [
            comment_service.get_insights_by_category(
                PositiveCommentCategory.MOTIVATIONAL,
                auth,
            )
            for _ in range(limit)
        ]
    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)
