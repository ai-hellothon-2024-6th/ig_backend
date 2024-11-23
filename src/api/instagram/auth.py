from src.api.instagram import get_graph_api, post_auth_api
from src.models.auth import *


def get_short_token(dto: LoginDTO):
    short_token_dto = ShortTokenRequestDTO(
        code=dto.code,
        redirect_uri=dto.redirect_uri,
    )
    short_token_response = post_auth_api(
        "/oauth/access_token",
        short_token_dto,
    )
    short_token_response["user_id"] = str(short_token_response["user_id"])
    return AuthDTO(**short_token_response)


def get_long_token(dto: AuthDTO):
    long_token_dto = LongTokenRequestDTO(
        access_token=dto.access_token,
    )
    long_token_response = get_graph_api(
        "/access_token",
        long_token_dto,
    )
    long_token_data = LongTokenResponseDTO(
        **long_token_response,
    )
    return AuthDTO(
        access_token=long_token_data.access_token,
        user_id=dto.user_id,
    )
