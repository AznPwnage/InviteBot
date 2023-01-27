import requests

from src.dao.ConfigDao import get_client_secret
from src.types.GrantType import GrantType


def call_oauth_token_api(code: str, grant_type: GrantType):
    url = 'https://www.bungie.net/platform/app/oauth/token/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    client_secret = get_client_secret()
    body = {'grant_type': grant_type.name,
            grant_type.code_type: code,
            'client_id': '35375',
            'client_secret': client_secret}

    response = requests.post(url, headers=headers, data=body)
    if response.status_code != 200:
        raise Exception

    return response
