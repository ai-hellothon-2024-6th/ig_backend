from fastapi import APIRouter, Response, Depends
from src.models.media import MediaDTO
from src.models.auth import AuthDTO
from src.api.instagram import media as media_api
from src.utils import jwt, responses
from requests.exceptions import HTTPError
from typing import List

# TODO : API와 DB 접점을 Service로 분리 (media)

router = APIRouter()


@router.get(
    "",
    response_model=List[MediaDTO],
    tags=["media"],
    responses={
        403: responses.forbidden,
    },
)
def media_list(auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        return media_api.get_media_list(auth)
    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )


@router.get(
    "/{media_id}",
    response_model=MediaDTO,
    tags=["media"],
    responses={
        403: responses.forbidden,
    },
)
def media_detail(
    media_id: str,
    auth: AuthDTO = Depends(jwt.verify_jwt),
):
    try:
        return media_api.get_media_detail(media_id, auth.access_token)
    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )
