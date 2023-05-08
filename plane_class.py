import json
import random
import string
import math
import time

from socket_connection import SocketConnection
import logging

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
        print(f"this is information about airplane_flight:{airplane_data}")
        time.sleep(2)
        return {"data": "request_landing_permission", **airplane_data}

    def receive_approach_permission(self, data):
        if data.get("airport_message", '') == "Permission to approach airport granted":
            self.permission_granted = True

    def request_runway_permission(self):
        airplane_data = self.airplane_flight.get_airplane_data()
        return {"data": "request_runway_permission", **airplane_data}

    def grant_permission_for_inbounding(self, data):
        print(f"here you have data get from airport. We should have message and permission granted")
        print(data)
        if data.get("message", '') == "permission granted":
            self.inbound = True
            return data
        else:
            runway_1_status = data.get("data", '').get("1", '')
            runway_2_status = data.get("data", '').get("2", '')
            print(f" runway_1_status: {runway_1_status}, 2: {runway_2_status}")
            return False

    def extract_runway_coordinates(self, data):
        runway_x = data.get("coordinates", '').get("x", '')
        runway_y = data.get("coordinates", '').get("y", '')
        runway_z = data.get("coordinates", '').get("z", '')
        return runway_x, runway_y, runway_z

    def send_landed_information(self):
        airplane_data = self.airplane_flight.get_airplane_data()
        return {"data": "confirm_landing", **airplane_data}
