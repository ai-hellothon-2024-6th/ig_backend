from fastapi import APIRouter, Response, Depends
from src.models.auth import LoginDTO, TokenDTO, AuthDTO
from src.api.instagram import auth as auth_api
from src.utils import jwt, responses
from requests.exceptions import HTTPError

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
        response = auth_api.get_access_token(dto)
        # access_token은 차후 장기 토큰으로 변환 후 db에 저장할 예정
        jwt_token = jwt.create_jwt_token(
            {"user_id": response.user_id, "access_token": response.access_token},
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
