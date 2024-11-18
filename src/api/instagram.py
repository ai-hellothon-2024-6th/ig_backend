from src.models.auth import *
from src.models.info import *
import requests


def get_access_token(dto: LoginDTO):
    def get_short_access_token(dto: ShortAccessTokenRequestDTO):
        url = "https://api.instagram.com/oauth/access_token"
        response = requests.post(url, data=dto.model_dump())
        response.raise_for_status()
        data = AccessTokenResponseDTO(**response.json())
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
    return AccessTokenResponseDTO(
        access_token=long_data.access_token, user_id=short_data.user_id
    )


def get_info(auth: AccessTokenResponseDTO):
    def get_me(dto: MeRequestDTO):
        url = "https://graph.instagram.com/me"
        response = requests.get(url, params=dto.model_dump())
        response.raise_for_status()
        data = response.json()
        return MeResponseDTO(**data)

    me = get_me(
        MeRequestDTO(
            access_token=auth.access_token,
            fields="username,name,account_type,followers_count",
        )
    )

    return InfoDTO(
        username=me.username,
        name=me.name,
        account_type=me.account_type,
        followers_count=me.followers_count,
    )
