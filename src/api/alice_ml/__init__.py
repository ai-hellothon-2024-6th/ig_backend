import uuid
from pydantic import BaseModel
from src.settings import settings
from src.api import post_api
from src.models.alice_ml import *

API = "https://api-cloud-function.elice.io"


def post_ml_api(path: str, dto: BaseModel) -> dict:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.ALICE_ML_API_KEY}",
    }
    response = post_api(f"{API}{path}", json=dto.model_dump(), headers=headers)
    return response


def get_scores(text: list[str]) -> list[ScoreResponseDTO]:
    response = post_ml_api(
        "/cf3b3742-4bf5-433b-9042-bc8c563c25cc/predict",
        ScoreRequestDTO(text=text),
    )
    return [ScoreResponseDTO(**el) for el in response]


def get_filterd_text(text: str) -> str:
    response = post_ml_api(
        "/d92f3aff-c80d-436f-ab07-75b1504d0019/v1/generate",
        FilteredTextRequestDTO(text=text, tone="honorific"),
    )
    return FilteredTextResponseDTO(**response).output


def get_generative_text(messages: list[dict]) -> str:
    # print("get_generative_text")
    response = post_ml_api(
        "/5a327f26-cc55-45c5-92b7-e909c2df0ba4/v1/chat/completions",
        GenerativeTextRequestDTO(sess_id=str(uuid.uuid4()), messages=messages),
    )
    # print("post_ml_api")
    return (
        GenerativeTextResponseDTO(**response).choices[0].get("message").get("content")
    )
