from enum import Enum

from src.enums.Region import Region
from src.types.Clan import Clan


class Clans(Enum):
    emerald = Clan('3640796', Region.NA)
    jade = Clan('3892235', Region.NA)
    peridot = Clan('4381485', Region.NA)
    beryl = Clan('4381489', Region.NA)
    olivine = Clan('4947412', Region.NA)
    ruby = Clan('3759206', Region.EU)
    garnet = Clan('3893809', Region.EU)
    thulite = Clan('4382110', Region.OCE)
    onyx = Clan('3893887', Region.INT)
    diamond = Clan('4315576', Region.INT)

    @classmethod
    def get_clan_names(cls):
        return list(map(lambda c: c.name, cls))
