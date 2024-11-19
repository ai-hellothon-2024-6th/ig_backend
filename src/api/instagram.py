import requests

from src.models.common import *
from src.models.auth import *
from src.models.info import *
from src.models.media import *
from src.utils.tools import fields

API = "https://api.instagram.com"
GRAPH = "https://graph.instagram.com"


def get_api(base_url: str, path: str, dto: BaseModel) -> dict:
    response = requests.get(f"{base_url}{path}", params=dto.model_dump())
    response.raise_for_status()
    return response.json()


def post_api(base_url: str, path: str, dto: BaseModel) -> dict:
    response = requests.post(f"{base_url}{path}", data=dto.model_dump())
    response.raise_for_status()
    return response.json()


def get_access_token(dto: LoginDTO):
    short_dto = ShortAccessTokenRequestDTO(code=dto.code, redirect_uri=dto.redirect_uri)
    short_response = post_api(API, "/oauth/access_token", short_dto)
    short_response["user_id"] = str(short_response["user_id"])
    short_data = AuthDTO(**short_response)
    long_dto = LongLivedAccessTokenRequestDTO(access_token=short_data.access_token)
    long_data = LongLivedAccessTokenResponseDTO(
        **get_api(GRAPH, "/access_token", long_dto)
    )
    return AuthDTO(access_token=long_data.access_token, user_id=short_data.user_id)


def get_info(auth: AuthDTO):
    fieldsDTO = RequestWithFieldsDTO(
        access_token=auth.access_token,
        fields=fields("username", "name", "account_type", "followers_count"),
    )
    return InfoDTO(**get_api(GRAPH, "/me", fieldsDTO))


def get_profile_info(auth: AuthDTO):
    fieldsDTO = RequestWithFieldsDTO(
        access_token=auth.access_token,
        fields=fields("profile_picture_url", "name", "username"),
    )
    return ProfileInfoDTO(**get_api(GRAPH, "/me", fieldsDTO))


def get_media_detail(media_id: str, access_token: str):
    fieldsDTO = RequestWithFieldsDTO(
        access_token=access_token,
        fields=fields(
            "caption",
            "media_url",
            "thumbnail_url",
            "like_count",
            "comments_count",
            "media_type",
            "timestamp",
        ),
    )
    data = get_api(GRAPH, f"/{media_id}", fieldsDTO)
    return MediaDTO(
        id=media_id,
        caption=data.get("caption") or "",
        media_url=data["media_url"],
        thumbnail_url=data.get("thumbnail_url") or data.get("media_url"),
        like_count=data["like_count"],
        comments_count=data["comments_count"],
        media_type=data["media_type"],
        timestamp=data["timestamp"],
    )


def get_media_list(auth: AuthDTO):
    return [
        get_media_detail(el["id"], auth.access_token)
        for el in get_api(GRAPH, "/me/media", auth)["data"]
    ]
