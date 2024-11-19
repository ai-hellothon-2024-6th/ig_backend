from pydantic import BaseModel


class MediaDTO(BaseModel):
    id: str
    thumbnail_url: str = None
    like_count: int = None
    comments_count: int = None
    caption: str = None
    media_type: str = None
    timestamp: str = None
