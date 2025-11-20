from enum import Enum


class RoleEnum(str, Enum):
    MEMBER = "MEMBER"
    ORG_ADMIN = "ORG_ADMIN"
    ADMIN = "ADMIN"


class Complexity(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class ChallengeStatus(str, Enum):
    ONGOING = "ONGOING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class ChannelEnum(str, Enum):
    EMAIL = "EMAIL"


class EmailRole(str, Enum):
    HOOK = "HOOK"
    USER = "USER"
    AI = "AI"
