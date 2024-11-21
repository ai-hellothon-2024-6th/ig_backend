from pydantic import BaseModel


class CommentDTO(BaseModel):
    id: str
    text: str
    timestamp: str  # UTC+0
    user: bool  # True: app user, False: other user
    username: str = None
    toxicity: bool = None  # True: 부정적 댓글, False: 긍정적 댓글
    filtered: str = ""  # 부정적 댓글에만 포함, 긍정적 댓글은 빈 문자열


class ReplyRecommendationDTO(BaseModel):
    reply: str
