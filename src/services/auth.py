import datetime
from src.models.auth import AuthDTO, LoginDTO
from src.db import auth as auth_repo
from src.api.instagram import auth as auth_api
from src.utils import tools
from src.services import media as media_service
from src.services import comment as comment_service


def get_auth_dto(dto: LoginDTO) -> AuthDTO:
    short_token = auth_api.get_short_token(dto)
    saved_token = auth_repo.find_auth_token_valid(short_token.user_id)
    if saved_token:
        # print("** 만료되지 않은 장기 토큰 존재")
        return AuthDTO(
            user_id=saved_token.ig_id,
            access_token=saved_token.token,
        )

    long_token = auth_api.get_long_token(short_token)

    auth_repo.save_auth_token(
        ig_id=long_token.user_id,
        token=long_token.access_token,
        valid_until=(tools.utcnow() + tools.timedelta(days=30)).strftime(
            "%Y-%m-%d %H:%M:%S",
        ),
    )
    # print("** 신규 장기 토큰 저장")

    return long_token


def delete_auth_token(user_id: str):
    auth_repo.delete_auth_token(user_id)


def sync_user_data(user_id: str):
    access_token = auth_repo.find_auth_token_valid(user_id).token
    media_list = media_service.get_media_list(
        AuthDTO(access_token=access_token, user_id=user_id)
    )
    media_service.save_media_list(media_list, user_id)

    for media in media_list:
        comment_service.sync_others_comments(
            media.id, AuthDTO(access_token=access_token, user_id=user_id)
        )
