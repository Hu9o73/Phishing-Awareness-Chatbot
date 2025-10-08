from enum import Enum

class RoleEnum(str, Enum):
    MEMBER = "MEMBER"
    ORG_ADMIN = "ORG_ADMIN"
    ADMIN = "ADMIN"
