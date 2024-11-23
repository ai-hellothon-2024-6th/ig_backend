from pydantic import BaseModel
from enum import Enum


class PositiveCommentCategory(str, Enum):
    EMOTIONAL = "emotional"
    MOTIVATIONAL = "motivational"
    NEUTRAL = "neutral"


class Comment(BaseModel):
    id: str
    text: str
    timestamp: str  # UTC+0
    username: str = None


class PositiveCommentDTO(Comment):
    category: PositiveCommentCategory


class CommentDTO(Comment):
    user: bool  # True: app user, False: other user
    toxicity: bool = None  # True: 부정적 댓글, False: 긍정적 댓글
    filtered: str = ""  # 부정적 댓글에만 포함, 긍정적 댓글은 빈 문자열
    like_count: int


class ReplyRecommendationDTO(BaseModel):
    id: str
    reply: str


class CommentSummaryDTO(BaseModel):
    text: str
    timestamp: str  # UTC+0


class CommentInsightDTO(BaseModel):
    text: str
    timestamp: str  # UTC+0
