from enum import Enum


class Status(Enum):
    WAITING = 1
    APPROACHING = 2
    DESCENDING = 3
    LANDED = 4
    CRASHED = 5


class AirplaneAction(Enum):
    REQUEST_APPROACHING_AIRPORT_PERMISSION = "request_approaching_airport_permission"
    REQUEST_RUNWAY_PERMISSION = "request_runway_permission"
    CONFIRM_LANDING = "confirm_landing"
