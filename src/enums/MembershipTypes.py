from enum import Enum

from src.types.MembershipType import MembershipType


class MembershipTypes(Enum):
    XBOX = MembershipType('xbox', '1', 'xb')
    PS = MembershipType('ps', '2', 'ps')
    STEAM = MembershipType('steam', '3', 'pc')
