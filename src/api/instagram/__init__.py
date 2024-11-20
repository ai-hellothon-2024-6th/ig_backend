import requests
from pydantic import BaseModel
from src.api import get_api, post_api

AUTH = "https://api.instagram.com"
GRAPH = "https://graph.instagram.com"


def get_graph_api(path: str, dto: BaseModel) -> dict:
    return get_api(f"{GRAPH}{path}", dto.model_dump())


def post_auth_api(path: str, dto: BaseModel) -> dict:
    return post_api(f"{AUTH}{path}", dto.model_dump())
