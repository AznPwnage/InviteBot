import requests

from src.dao.ConfigDao import get_api_key


def send_invite(membership_type: str, membership_id: str, clan_id: str, access_token: str):
    url = 'https://www.bungie.net/platform/groupv2/' + clan_id + '/members/individualinvite/' + membership_type + '/' + membership_id
    authorization_value = 'Bearer ' + access_token
    headers = {'x-api-key': get_api_key(), 'authorization': authorization_value, 'content-type': 'text/plain'}
    body = '{}'

    response = requests.post(url, headers=headers, data=body)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception
    return
