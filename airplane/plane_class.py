import random
import logging
from airplane.airplane_flight import AirplaneFlight
from socket_connection import SocketConnection
from airplane.unique_generator import UniqueIDGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Airplane(SocketConnection):
    unique_ids = set()

    def __init__(self, socket=None):
        super().__init__(socket_instance=socket)

        self.airplane_flight = None
        self.socket.connect((self.host, self.port))
        self.init_airplane_state()
        self.permission_granted = None
        self.inbound = None

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

    def request_landing_permission(self):
        airplane_data = self.airplane_flight.get_airplane_data()
        return {"data": "request_landing_permission", **airplane_data}

    def receive_approach_permission(self, data):
        if data.get("airport_message", '') == "Permission to approach airport granted":
            self.permission_granted = True

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
