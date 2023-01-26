from enum import Enum

from src.types.GrantType import GrantType


class GrantTypes(Enum):
    AuthorizationCode = GrantType('authorization_code', 'code')
    RefreshToken = GrantType('refresh_token', 'refresh_token')