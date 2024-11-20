from src.api.instagram import get_graph_api
from src.models.comment import CommentDTO
from src.models.common import RequestWithFieldsDTO, OnlyAccessTokenDTO
from src.utils.tools import fields


def get_comments(media_id: str, access_token: str):
    api_response = get_graph_api(
        f"/{media_id}/comments",
        OnlyAccessTokenDTO(access_token=access_token),
    )
    return [el["id"] for el in api_response["data"]]


def get_comment_detail(comment_id: str, access_token: str):
    keys = list(CommentDTO.model_fields.keys())
    keys.remove("toxicity")
    keys.remove("filtered")
    fieldsDTO = RequestWithFieldsDTO(
        access_token=access_token,
        fields=fields(*keys),
    )
    response = get_graph_api(f"/{comment_id}", fieldsDTO)
    response["user"] = response.get("user") is not None
    return CommentDTO(**response)
