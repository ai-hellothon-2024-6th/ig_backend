from src.api.instagram import get_graph_api
from src.models.common import RequestWithFieldsDTO
from src.models.auth import AuthDTO
from src.models.media import MediaDTO
from src.utils.tools import fields


def get_media_detail(media_id: str, access_token: str):
    fieldsDTO = RequestWithFieldsDTO(
        access_token=access_token,
        fields=fields(*MediaDTO.model_fields.keys(), "media_url"),
    )
    data = get_graph_api(f"/{media_id}", fieldsDTO)
    data["thumbnail_url"] = data.get("thumbnail_url") or data.get("media_url")
    data["caption"] = data.get("caption") or ""
    return MediaDTO(**data)


def get_media_list(auth: AuthDTO):
    return [
        get_media_detail(el["id"], auth.access_token)
        for el in get_graph_api("/me/media", auth)["data"]
    ]
