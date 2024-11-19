from src.models.common import *
from src.models.auth import *
from src.models.info import *
from src.models.media import *
import requests


def get_access_token(dto: LoginDTO):
    def get_short_access_token(dto: ShortAccessTokenRequestDTO):
        url = "https://api.instagram.com/oauth/access_token"
        response = requests.post(url, data=dto.model_dump())
        response.raise_for_status()
        data = AuthDTO(**response.json())
        return data

    def get_long_lived_access_token(dto: LongLivedAccessTokenRequestDTO):
        url = "https://graph.instagram.com/access_token"
        response = requests.get(url, params=dto.model_dump())
        response.raise_for_status()
        data = LongLivedAccessTokenResponseDTO(**response.json())
        return data

    short_data = get_short_access_token(
        ShortAccessTokenRequestDTO(code=dto.code, redirect_uri=dto.redirect_uri)
    )
    long_data = get_long_lived_access_token(
        LongLivedAccessTokenRequestDTO(access_token=short_data.access_token)
    )
    return AuthDTO(access_token=long_data.access_token, user_id=short_data.user_id)


def get_info(auth: AuthDTO):
    url = "https://graph.instagram.com/me"
    response = requests.get(
        url,
        params=RequestWithFieldsDTO(
            access_token=auth.access_token,
            fields="username,name,account_type,followers_count",
        ).model_dump(),
    )
    response.raise_for_status()
    data = response.json()
    return InfoDTO(**data)


def get_profile_info(auth: AuthDTO):
    url = "https://graph.instagram.com/me"
    response = requests.get(
        url,
        params=RequestWithFieldsDTO(
            access_token=auth.access_token,
            fields=",".join(["profile_picture_url", "name", "username"]),
        ).model_dump(),
    )
    response.raise_for_status()
    data = response.json()
    return ProfileInfoDTO(**data)


def get_media_detail(media_id: str, access_token: str):
    url = f"https://graph.instagram.com/{media_id}"
    response = requests.get(
        url,
        params=RequestWithFieldsDTO(
            access_token=access_token,
            fields=",".join(
                [
                    "caption",
                    "media_url",
                    "thumbnail_url",
                    "like_count",
                    "comments_count",
                ]
            ),
        ).model_dump(),
    )
    response.raise_for_status()
    data: dict = response.json()
    return MediaDTO(
        id=media_id,
        thumbnail_url=data.get("thumbnail_url") or data.get("media_url"),
        like_count=data.get("like_count"),
        comments_count=data.get("comments_count"),
        caption=data.get("caption") or "",
    )


def get_media_list(auth: AuthDTO):
    url = "https://graph.instagram.com/me/media"
    response = requests.get(url, params={"access_token": auth.access_token})
    response.raise_for_status()
    data = response.json()
    return [get_media_detail(el["id"], auth.access_token) for el in data["data"]]
