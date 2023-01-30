from enum import Enum


class Clans(Enum):
    Emerald = '3640796'
    Jade = '3892235'
    Peridot = '4381485'
    Beryl = '4381489'
    Ruby = '3759206'
    Garnet = '3893809'
    Thulite = '4382110'
    Onyx = '3893887'
    Diamond = '4315576'

    @classmethod
    def get_clan_names(cls):
        return list(map(lambda c: c.name, cls))
