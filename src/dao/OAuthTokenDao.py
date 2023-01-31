import pickle

import requests

from src.business.OAuthTokenHandler import handle_oauth_token
from src.dao.ConfigDao import get_client_secret
from src.enums.Clans import Clans
from src.types.GrantType import GrantType
from src.types.OAuthToken import OAuthToken


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


def get_oauth_token(clan: Clans):
    with open('src/tokens/' + clan.name, 'rb') as token_file:
        oauth_token = pickle.load(token_file)

    return handle_oauth_token(clan, oauth_token)


def save_oauth_token(clan: Clans, oauth_token: OAuthToken):
    with open('src/tokens/' + clan.name, 'wb') as token_file:
        pickle.dump(oauth_token, token_file)
