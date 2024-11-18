from pydantic import BaseModel

class InfoDTO(BaseModel):
    name: str
    username: str
    account_type: str
    followers_count: int

class MeRequestDTO(BaseModel):
    access_token: str
    fields: str

class MeResponseDTO(BaseModel):
    username: str
    name: str
    account_type: str
    followers_count: int