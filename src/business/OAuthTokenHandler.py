import pickle
import time

from src.dao.OAuthTokenDao import call_oauth_token_api
from src.enums.Clans import Clans
from src.enums.GrantTypes import GrantTypes
from src.types.OAuthToken import OAuthToken


def get_oauth_token(clan: Clans):
    with open('src/tokens/' + clan.name, 'rb') as token_file:
        oauth_token = pickle.load(token_file)

    return handle_oauth_token(clan, oauth_token)


def save_oauth_token(clan: Clans, oauth_token: OAuthToken):
    with open('src/tokens/' + clan.name, 'wb') as token_file:
        pickle.dump(oauth_token, token_file)


def handle_oauth_token(clan: Clans, oauth_token: OAuthToken):
    current_time = time.time()

    if oauth_token.expires_at_seconds > current_time:
        return oauth_token

    response = call_oauth_token_api(oauth_token.refresh_token, GrantTypes.RefreshToken.value)

    oauth_token = convert_response_to_oauth_token(response.json())
    save_oauth_token(clan, oauth_token)

    return oauth_token


def convert_response_to_oauth_token(response_json):
    current_time = time.time()

    expires_at_seconds = current_time + response_json['expires_in']
    refresh_expires_at_seconds = current_time + response_json['refresh_expires_in']

    oauth_token = OAuthToken(response_json['access_token'],
                             response_json['token_type'],
                             expires_at_seconds,
                             response_json['refresh_token'],
                             refresh_expires_at_seconds,
                             response_json['membership_id'])
    return oauth_token
