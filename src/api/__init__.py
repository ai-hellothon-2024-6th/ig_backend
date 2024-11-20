import requests


def get_api(url: str, params: dict) -> dict:
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def post_api(url: str, payload: dict, headers: dict = None) -> dict:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
