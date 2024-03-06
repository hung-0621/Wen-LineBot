import requests


def get_response_from_url(url) -> str:
    response = requests.get(url=url)
    return response.text
