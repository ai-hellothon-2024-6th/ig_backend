from fastapi import APIRouter, Response, Depends
from src.models.info import *
from src.models.auth import AccessTokenResponseDTO
from src.api import instagram
from src.utils import jwt
from requests.exceptions import HTTPError

info_router = APIRouter()


@info_router.get(
    "/",
    response_model=InfoDTO,
    tags=["info"],
    responses={
        403: {
            "description": "Forbidden",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
    },
)
def info(auth: AccessTokenResponseDTO = Depends(jwt.verify_jwt)):
    try:
        return instagram.get_info(auth)
    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)
