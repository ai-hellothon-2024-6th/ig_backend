from pydantic import BaseModel


class InfoDTO(BaseModel):
    username: str
    name: str
    account_type: str
    followers_count: int


class ProfileInfoDTO(BaseModel):
    profile_picture_url: str
    name: str
    username: str
