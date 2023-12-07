from enum import Enum


class AccountType(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMINISTRATOR = "administrator"
