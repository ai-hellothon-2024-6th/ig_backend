from typing import List
from pydantic import BaseModel


class ScoreRequestDTO(BaseModel):
    text: List[str]


class ScoreResponseDTO(BaseModel):
    is_toxic: bool
    score: float


class FilteredTextRequestDTO(BaseModel):
    tone: str
    text: str


class FilteredTextResponseDTO(BaseModel):
    output: str


class GenerativeTextRequestDTO(BaseModel):
    model: str = "helpy-pro"
    sess_id: str  # UUIDv4
    messages: List[dict]
    max_tokens: int = 512


class GenerativeTextResponseDTO(BaseModel):
    choices: List[dict]
