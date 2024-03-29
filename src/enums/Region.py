from enum import Enum


class Region(Enum):
    NA = 'NA <:OBWS_NA:885217965287551006>'
    EU = 'EU <:OBWS_EU:885217965258178640>'
    OCE = 'OCE <:OBWS_OCE_ASIA:885217965216251964>'
    INT = 'INT <:OBWS_Raid:885217965140762744>'

    @classmethod
    def get_region_names(cls):
        return list(map(lambda c: c.name, cls))
