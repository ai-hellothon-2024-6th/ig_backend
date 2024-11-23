from fastapi import APIRouter, Response, Depends
from src.models.auth import LoginDTO, TokenDTO, AuthDTO
from src.services import auth as auth_service
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
        response = auth_service.get_auth_dto(dto)
        auth_service.sync_user_data(response.user_id)
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
        auth_service.delete_auth_token(auth.user_id)
        return {"message": "logout success"}
    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )
