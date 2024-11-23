from requests import HTTPError
from fastapi import Response
from src.models.auth import AuthDTO
from src.api.instagram import info as info_api
from src.db import auth as auth_db


def get_profile_info(auth: AuthDTO):
    try:
        authTokens = auth_db.find_auth_token_valid(auth.user_id)
        auth.access_token = authTokens.token
        return info_api.get_profile_info(auth)
    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )


def get_info(auth: AuthDTO):
    try:
        authTokens = auth_db.find_auth_token_valid(auth.user_id)
        auth.access_token = authTokens.token
        return info_api.get_info(auth)
    except HTTPError as e:
        return Response(
            content=e.response.text,
            status_code=e.response.status_code,
        )
