from pydantic import BaseModel


class RequestWithFieldsDTO(BaseModel):
    access_token: str
    fields: str
