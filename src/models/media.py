from pydantic import BaseModel


class MediaDTO(BaseModel):
    id: int
    thumbnail_url: str = None
    like_count: int = None
    comments_count: int = None
    caption: str = None
