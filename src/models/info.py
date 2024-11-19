from pydantic import BaseModel


class InfoDTO(BaseModel):
    name: str
    username: str
    account_type: str
    followers_count: int


class MeResponseDTO(BaseModel):
    username: str
    name: str
    account_type: str
    followers_count: int
