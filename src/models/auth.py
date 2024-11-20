from pydantic import BaseModel
from src.settings import settings


class LoginDTO(BaseModel):
    code: str
    redirect_uri: str
    expires_seconds: int = 60 * 60 * 24  # 개발 편의상 수정 가능
    # 배포 시에는 아예 삭제하고 고정값으로 설정


class ShortTokenRequestDTO(BaseModel):
    client_id: int = settings.IG_CLIENT_ID
    client_secret: str = settings.IG_CLIENT_SECRET
    grant_type: str = settings.IG_GRANT_TYPE
    redirect_uri: str
    code: str


class AuthDTO(BaseModel):
    access_token: str
    user_id: str


class LongTokenRequestDTO(BaseModel):
    grant_type: str = "ig_exchange_token"
    client_secret: str = settings.IG_CLIENT_SECRET
    access_token: str


class LongTokenResponseDTO(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenDTO(BaseModel):
    token: str
