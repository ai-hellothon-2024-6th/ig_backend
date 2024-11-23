import datetime
from src.models.auth import AuthDTO, LoginDTO
from src.db.auth import save_auth_token, find_auth_token
from src.api.instagram import auth as auth_api
from src.utils import tools


def get_auth_dto(dto: LoginDTO) -> AuthDTO:
    short_token = auth_api.get_short_token(dto)
    saved_token = find_auth_token(short_token.user_id)
    if saved_token:
        print("** 만료되지 않은 장기 토큰 존재")
        return AuthDTO(
            user_id=saved_token.ig_id,
            access_token=saved_token.token,
        )

    long_token = auth_api.get_long_token(short_token)

    save_auth_token(
        ig_id=long_token.user_id,
        token=long_token.access_token,
        valid_until=(tools.utcnow() + tools.timedelta(days=30)).strftime(
            "%Y-%m-%d %H:%M:%S",
        ),
    )
    print("** 신규 장기 토큰 저장")

    return long_token
