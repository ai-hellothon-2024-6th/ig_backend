from pydantic import BaseModel


class MediaDTO(BaseModel):
    id: str
    thumbnail_url: str
    like_count: int
    comments_count: int
    caption: str
    media_type: str
    timestamp: str
