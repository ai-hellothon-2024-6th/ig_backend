from fastapi import APIRouter, Response, Depends
from src.models.info import *
from src.models.auth import AuthDTO
from src.api import instagram
from src.utils import jwt, responses
from requests.exceptions import HTTPError

info_router = APIRouter()


@info_router.get(
    "/profile",
    response_model=ProfileInfoDTO,
    tags=["info"],
    responses={
        403: responses.forbidden,
    },
)
def profile_info(auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        return instagram.get_profile_info(auth)
    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


@info_router.get(
    "",
    response_model=InfoDTO,
    tags=["info"],
    responses={
        403: responses.forbidden,
    },
)
def info(auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        return instagram.get_info(auth)
    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)
