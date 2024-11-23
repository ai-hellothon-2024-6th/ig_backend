from src.api.instagram import media as media_api
from src.models.auth import AuthDTO
from src.db import auth as auth_db
from src.db.media import UserMedia
from src.db import media as media_db
from src.models.media import MediaDTO


def get_media_list(auth: AuthDTO):
    authTokens = auth_db.find_auth_token_valid(auth.user_id)
    auth.access_token = authTokens.token
    return media_api.get_media_list(auth)


def get_media_detail(media_id: str, auth: AuthDTO):
    authTokens = auth_db.find_auth_token_valid(auth.user_id)
    return media_api.get_media_detail(media_id, authTokens.token)


def save_media_list(user_media: list[MediaDTO], user_id: str):
    media_db.save_user_media(user_media, user_id)
