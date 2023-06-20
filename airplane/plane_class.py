import random
import logging
from .airplane_flight import AirplaneFlight
from socket_connection import SocketConnection
from .airplane_enums import Status, AirplaneAction
from .unique_generator import UniqueIDGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Airplane(SocketConnection):
    unique_ids = set()

    def __init__(self, socket=None):
        super().__init__(socket_instance=socket)
        self.airplane_flight = None
        self.socket.connect((self.host, self.port))
        self.init_airplane_state()
        self.status = Status.WAITING

    def __str__(self):
        airplane = self.airplane_flight.get_airplane_data()
        return f"{airplane}"

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
        return {"data": AirplaneAction.REQUEST_APPROACHING_AIRPORT_PERMISSION.value, **airplane_data}

    def receive_approach_permission(self, data):
        if self.status != Status.WAITING:
            raise ValueError("Airplane is not in appropriate status to receive approach permission.")

        if data.get("airport_message", '') == "Permission to approach airport granted":
            self.set_status(Status.APPROACHING)

    def request_runway_permission(self):
        if self.status != Status.APPROACHING:
            raise ValueError("Airplane is not in appropriate status to receive runway permission.")
        airplane_data = self.airplane_flight.get_airplane_data()
        return {"data": AirplaneAction.REQUEST_RUNWAY_PERMISSION.value, **airplane_data}

    def receive_permission_to_descending(self, data):
        if data.get("airport_message", '') == "permission for approaching runway granted":
            self.set_status(Status.DESCENDING)
            runway_coordinates = self._extract_runway_coordinates(data)
            self.airplane_flight.runway_coordinates = runway_coordinates
        else:
            return False

    def _extract_runway_coordinates(self, data):
        runway_x = data.get("coordinates", {}).get("x")
        runway_y = data.get("coordinates", {}).get("y")
        runway_z = data.get("coordinates", {}).get("z")
        return runway_x, runway_y, runway_z

    def send_landed_information(self):
        airplane_data = self.airplane_flight.get_airplane_data()
        return {"data": AirplaneAction.CONFIRM_LANDING.value, **airplane_data}
