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
