forbidden = {
    "description": "Forbidden",
    "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
}

bad_request_ig = {
    "description": "Bad Request",
    "content": {
        "application/json": {
            "example": {
                "error_type": "OAuthException",
                "code": 400,
                "error_message": "Matching code was not found or was already used",
            }
        }
    },
}

logoutSuccess = {
    "description": "Logout Success",
    "content": {
        "application/json": {
            "example": {
                "message": "logout success",
            }
        }
    },
}
