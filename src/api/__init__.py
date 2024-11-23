import requests


def get_api(url: str, params: dict) -> dict:
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def post_api(
    url: str,
    json: dict = None,
    data: dict = None,
    params: dict = None,
    headers: dict = None,
) -> dict:
    response = requests.post(url, params=params, data=data, json=json, headers=headers)
    response.raise_for_status()
    return response.json()
