import random
import logging
from .airplane_flight import AirplaneFlight
from socket_connection import SocketConnection
from .unique_generator import UniqueIDGenerator
from enum import Enum

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Status(Enum):
    WAITING = 1
    APPROACHING = 2
    DESCENDING = 3
    LANDED = 4
    CRASHED = 5


class Airplane(SocketConnection):
    unique_ids = set()

    def __init__(self, socket=None):
        super().__init__(socket_instance=socket)

        self.airplane_flight = None
        self.socket.connect((self.host, self.port))
        self.init_airplane_state()
        self.permission_granted = None
        self.inbound = None
        self.status = Status.WAITING

    def __str__(self):
        a = self.airplane_flight.get_airplane_data()
        return f"{a}"

    def init_airplane_state(self):
        x = random.randint(-5000, 5000)
        y = random.randint(-5000, 5000)
        z = random.randint(2000, 5000)
        velocity = random.randint(50, 500)
        fuel = random.randint(0, 1000)
        uniqueID = UniqueIDGenerator.generate_unique_id()
        self.airplane_flight = AirplaneFlight(uniqueID, x, y, z, velocity, fuel, self)

    def set_status(self, status):
        if isinstance(status, Status):
            self.status = status
        else:
            raise ValueError("Invalid Airplane status")

    def request_landing_permission(self):
        airplane_data = self.airplane_flight.get_airplane_data()
        return {"data": "request_landing_permission", "status": self.status.name, **airplane_data}

    def receive_approach_permission(self, data):
        if self.status != Status.WAITING:
            raise ValueError("Airplane is not in appropriate status to receive approach permission.")

        if data.get("airport_message", '') == "Permission to approach airport granted":
            self.permission_granted = True
            self.set_status(Status.APPROACHING)

    def request_runway_permission(self):
        airplane_data = self.airplane_flight.get_airplane_data()
        return {"data": "request_runway_permission", **airplane_data}

    def grant_permission_for_inbounding(self, data):
        if data.get("airport_message", '') == "permission granted":
            self.inbound = True
            return data
        else:
            return False

    def extract_runway_coordinates(self, data):
        runway_x = data.get("coordinates", {}).get("x")
        runway_y = data.get("coordinates", {}).get("y")
        runway_z = data.get("coordinates", {}).get("z")
        return runway_x, runway_y, runway_z

    def send_landed_information(self):
        airplane_data = self.airplane_flight.get_airplane_data()
        return {"data": "confirm_landing", **airplane_data}
