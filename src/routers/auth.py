from fastapi import APIRouter, Response, Depends
from src.models.auth import LoginDTO, TokenDTO, AuthDTO
from src.services.auth import get_auth_dto
from src.utils import jwt, responses
from requests.exceptions import HTTPError

# TODO : API와 DB 접점을 Service로 분리 (auth)

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenDTO,
    tags=["auth"],
    responses={
        400: responses.bad_request_ig,
    },
)
def login(dto: LoginDTO):
    try:
        response = get_auth_dto(dto)
        jwt_token = jwt.create_jwt_token(
            {"user_id": response.user_id},
            dto.expires_seconds,
        )
        return {"token": jwt_token}
    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )


@router.get(
    "/logout",
    tags=["auth"],
    responses={
        200: responses.logoutSuccess,
        403: responses.forbidden,
    },
)
def logout(auth: AuthDTO = Depends(jwt.verify_jwt)):
    try:
        # TODO : 저장된 access_token 삭제
        return {"message": "logout success"}
    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )
