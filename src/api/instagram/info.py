from src.api.instagram import get_graph_api
from src.models.common import RequestWithFieldsDTO
from src.models.auth import AuthDTO
from src.models.info import InfoDTO, ProfileInfoDTO
from src.utils.tools import fields


def get_info(auth: AuthDTO):
    fieldsDTO = RequestWithFieldsDTO(
        access_token=auth.access_token,
        fields=fields(*InfoDTO.model_fields.keys()),
    )
    return InfoDTO(**get_graph_api("/me", fieldsDTO))


def get_profile_info(auth: AuthDTO):
    fieldsDTO = RequestWithFieldsDTO(
        access_token=auth.access_token,
        fields=fields(*ProfileInfoDTO.model_fields.keys()),
    )
    return ProfileInfoDTO(**get_graph_api("/me", fieldsDTO))
