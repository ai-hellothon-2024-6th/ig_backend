from fastapi import APIRouter, Response
from src.models.auth import LoginDTO, TokenDTO
from src.api import instagram
from src.utils import jwt, responses
from requests.exceptions import HTTPError

auth_router = APIRouter()


@auth_router.post(
    "/login",
    response_model=TokenDTO,
    tags=["auth"],
    responses={
        400: responses.bad_request_ig,
    },
)
def login(dto: LoginDTO):
    try:
        response = instagram.get_access_token(dto)
        # access_token은 차후 장기 토큰으로 변환 후 db에 저장할 예정
        jwt_token = jwt.create_jwt_token(
            {"user_id": response.user_id, "access_token": response.access_token},
            dto.expires_seconds,
        )
        return {"token": jwt_token}
    except HTTPError as e:
        return Response(content=e.response.text, status_code=e.response.status_code)


# TODO: WEB01_UserData02 유저 말투 학습
# TODO: DB 연동
