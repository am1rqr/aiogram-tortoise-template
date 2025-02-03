from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "active"
    BANNED = "banned"


class AdLinkStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"