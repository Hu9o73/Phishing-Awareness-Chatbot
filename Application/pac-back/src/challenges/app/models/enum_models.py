from enum import Enum


class RoleEnum(str, Enum):
    MEMBER = "MEMBER"
    ORG_ADMIN = "ORG_ADMIN"
    ADMIN = "ADMIN"


class Complexity(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class EmailRole(str, Enum):
    HOOK = "HOOK"
    USER = "USER"
    AI = "AI"
