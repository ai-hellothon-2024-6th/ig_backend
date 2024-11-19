from fastapi import APIRouter, Response, Depends
from src.models.media import MediaDTO
from src.models.auth import AuthDTO
from src.api import instagram
from src.utils import jwt
from requests.exceptions import HTTPError
from typing import List

media_router = APIRouter()


@media_router.get(
    "/",
    response_model=List[MediaDTO],
    tags=["media"],
    responses={
        403: {
            "description": "Forbidden",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
    },
)
def media_list(auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        return instagram.get_media_list(auth)
    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)
