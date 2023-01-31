from src.dao.ClanInfoDao import get_clan_info
from src.enums.Clans import Clans
from src.utils.DictUtils import append_str_to_value_if_key_exists, append_obj_to_value_if_key_exists


def get_divisions_info_by_region_value(clan_info_dict):
    divisions_by_region = {}

    for division_name, clan_info in clan_info_dict.items():
        clan_region = Clans[division_name].value.region.value
        append_str_to_value_if_key_exists(divisions_by_region, '\n', clan_region, clan_info.pretty_print())

    return divisions_by_region


def get_divisions_by_region_name(clan_info_dict):
    divisions_by_region = {}

    for division_name, clan_info in clan_info_dict.items():
        clan_region = Clans[division_name].value.region.name
        append_obj_to_value_if_key_exists(divisions_by_region, clan_region, clan_info)

    return divisions_by_region


def get_smallest_division_group_id_by_region_name(region_name):
    clan_info_dict = get_clan_info()
    divisions_by_region = get_divisions_by_region_name(clan_info_dict)

    smallest_division_name = divisions_by_region.get(region_name).sort(key=lambda x: x.member_count).name

    return Clans[smallest_division_name].value.group_id
