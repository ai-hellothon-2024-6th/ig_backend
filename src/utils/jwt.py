from src.utils import tools
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from src.settings import settings
from src.models.auth import AuthDTO

bearer_scheme = HTTPBearer()


def create_jwt_token(data: dict, expires_seconds: int):
    to_encode = data.copy()
    expire = tools.utcnow() + tools.timedelta(seconds=expires_seconds)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_jwt_token(token: str):
    return AuthDTO(**jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"]))


def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        return decode_jwt_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
