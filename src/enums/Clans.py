from enum import Enum

from src.enums.ClanType import ClanType
from src.enums.Region import Region
from src.types.Clan import Clan


class Clans(Enum):
    emerald = Clan('3640796', Region.NA, ClanType.REGIONAL)
    jade = Clan('3892235', Region.NA, ClanType.REGIONAL)
    peridot = Clan('4381485', Region.NA, ClanType.REGIONAL)
    beryl = Clan('4381489', Region.NA, ClanType.REGIONAL)
    olivine = Clan('4947412', Region.NA, ClanType.REGIONAL)
    ruby = Clan('3759206', Region.EU, ClanType.REGIONAL)
    garnet = Clan('3893809', Region.EU, ClanType.REGIONAL)
    jasper = Clan('5027569', Region.EU, ClanType.REGIONAL)
    thulite = Clan('4382110', Region.OCE, ClanType.REGIONAL)
    onyx = Clan('3893887', Region.INT, ClanType.RAID)
    diamond = Clan('4315576', Region.INT, ClanType.RAID_ELITE)

    @classmethod
    def get_clan_names(cls):
        return list(map(lambda c: c.name, cls))
