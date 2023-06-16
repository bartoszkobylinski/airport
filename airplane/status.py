from enum import Enum


class Status(Enum):
    WAITING = 1
    APPROACHING = 2
    DESCENDING = 3
    LANDED = 4
    CRASHED = 5
