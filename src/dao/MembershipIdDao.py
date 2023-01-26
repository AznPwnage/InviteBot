import json

import requests

from src.dao.ConfigDao import get_api_key


def get_membership_id(bungie_name: str, membership_type: str):
    display_name, display_name_code = get_display_name_and_code(bungie_name)

    url = 'https://www.bungie.net/platform/destiny2/searchdestinyplayerbybungiename/' + membership_type
    headers = {'content-type': 'application/json', 'x-api-key': get_api_key()}
    body = json.dumps({'displayName': display_name, 'displayNameCode': display_name_code})

    response = requests.post(url, headers=headers, data=body)
    if response.status_code != 200:
        raise Exception

    return response.json()['Response'][0]['membershipId']


def get_display_name_and_code(bungie_name: str):
    split_list = bungie_name.split('#', 1)
    if len(split_list[1]) != 4:
        raise Exception('Bungie name code is not of length 4')

    return split_list[0], split_list[1]