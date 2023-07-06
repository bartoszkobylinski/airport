from enum import Enum


class Action(Enum):
    APPROACH_AIRPORT_PERMISSION = "request_approaching_airport_permission"
    EXECUTE_APPROACH = "execute_approach"
    RUNWAY_PERMISSION = "request_runway_permission"
    RUNWAY_APPROACH = "execute_runway_approach"
    CONFIRM_LANDING = "confirm_landing"
    UNKNOWN = "unknown"


class AirportResponse(Enum):
    APPROACH_AIRPORT_GRANTED = "Permission to approach airport_class granted"
    APPROACH_AIRPORT_REJECTED = "Permission to approach airport_class rejected"
    PERMISSION_GRANTED = "permission granted"
    PERMISSION_DENIED = "permission denied"
    AIRPLANE_LANDED = "airplane_class landed"
