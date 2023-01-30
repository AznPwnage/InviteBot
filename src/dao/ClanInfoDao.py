import os
import pickle
import time

import requests

from src.dao.ConfigDao import get_api_key
from src.enums.Clans import Clans
from src.types.ClanInfo import ClanInfo


def get_clan_info():
    clan_info_dict = {}
    for clan_name in Clans.get_clan_names():
        clan_info = read_clan_info(clan_name)

        if clan_info is None:
            clan_info = ClanInfo(clan_name, 0, True, time.time())

        clan_info.member_count = get_clan_member_count_from_bungie(Clans[clan_name].value.group_id)

        save_clan_info(clan_info)
        clan_info_dict.update({clan_name: clan_info})

    return clan_info_dict


def read_clan_info(clan_name):
    clan_info_file_path = 'resources/claninfo/' + clan_name

    try:
        if not os.path.exists(clan_info_file_path):
            return None
        with open(clan_info_file_path, 'rb') as clan_info_file:
            return pickle.load(clan_info_file)
    except Exception:
        print(Exception)


def save_clan_info(clan_info: ClanInfo):
    with open('resources/claninfo/' + clan_info.name, 'wb') as clan_info_file:
        pickle.dump(clan_info, clan_info_file)


def get_clan_member_count_from_bungie(clan_id: str):
    url = 'https://www.bungie.net/platform/groupv2/' + clan_id + '/members'
    headers = {'content-type': 'application/json', 'x-api-key': get_api_key()}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception

    return response.json()['Response']['totalResults']
