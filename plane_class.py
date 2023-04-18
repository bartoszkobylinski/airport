import json
import random
import string
import math
import time
import numpy as np
from socket_connection import SocketConnection
import logging

logging.basicConfig(level=logging.INFO)


class UniqueIDGenerator:
    unique_ids = set()

    @classmethod
    def generate_unique_id(cls):
        uniqueId = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while uniqueId in cls.unique_ids:
            uniqueId = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        cls.unique_ids.add(uniqueId)
        return uniqueId


class AirplaneFlight:
    def __init__(self, uniqueId, x, y, z, velocity, fuel):
        self.uniqueId = uniqueId
        self.x = x
        self.y = y
        self.z = z
        self.velocity = velocity
        self.fuel = fuel
        self.landed = False

    def calculate_distance(self, x, y, z):
        return np.linalg.norm(np.array([self.x, self.y, self.z]) - np.array([x, y, z]))

    def update_airplane_position(self, corridor_x, corridor_y, corridor_z, distance):
        if 100 < distance < 500:
            self.velocity = random.randint(10, 50)
        else:
            direction_vector = (np.array([corridor_x, corridor_y, corridor_z]) - np.array(
                [self.x, self.y, self.z])) / distance
            self.x += self.velocity * direction_vector[0]
            self.x = round(self.x, 0)
            self.y += self.velocity * direction_vector[1]
            self.y = round(self.y, 0)
            self.z += self.velocity * direction_vector[2]
            self.z = round(self.z, 0)
            self.fuel -= 1
            if self.fuel == 0:
                logging.error(f"Airplane {self.uniqueId} has run out of fuel and has collide")

    def fly_randomly(self):
        direction = random.randint(0, 360)
        self.x += self.velocity * math.cos(direction)
        self.x = round(self.x, 0)
        self.y += self.velocity * math.sin(direction)
        self.y = round(self.y, 0)
        self.z += self.velocity * math.sin(direction)
        self.z = round(self.z, 0)
        return {"data": "fly", "x": self.x, "y": self.y, "z": self.z}

    def fly_to_corridor(self, corridor_x, corridor_y, corridor_z):
        distance = self.calculate_distance(corridor_x, corridor_y, corridor_z)
        logging.info(f"Airplane {self.uniqueId} is {round(distance, 0)} meters away from the corridor")
        time.sleep(1.5)

        if distance <= 100:
            self.handle_entered_corridor()
            return {"data": "landed"}
        else:
            self.update_airplane_position(corridor_x, corridor_y, corridor_z, distance)
            return {"data": "inbound", "x": self.x, "y": self.y, "z": self.z}

    def handle_entered_corridor(self):
        logging.info(f"Airplane {self.uniqueId} has entered the corridor")
        self.landed = True


class Airplane(SocketConnection):
    unique_ids = set()

    def __init__(self):
        super().__init__()

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
        self.airplane_flight = AirplaneFlight(uniqueID, x, y, z, velocity, fuel)

    def send_json(self, data, airplane_id=None):
        if airplane_id is None:
            airplane_id = self.airplane_flight.uniqueId
        data_to_send = {"airplane_ID": airplane_id} | data
        json_data = json.dumps(data_to_send)
        self.socket.send(json_data.encode(self.encoder))

    def recv_json(self):
        data = self.socket.recv(self.buffer)
        if data:
            json_data = json.loads(data.decode(self.encoder))
            return json_data
        else:
            self.socket.close()



    def send_landed_information(self):
        return {"data": "landed", "coordinates": {"x": self.x, "y": self.y, "z": self.z}}

    def send_inbound_coordinates(self):
        return {"data": "inbound", "coordinates": {"x": self.x, "y": self.y, "z": self.z}}

    def recieve_permission(self, data):
        if data:
            self.permission_granted = True
        else:
            del self

    def recieve_permisssion_for_inbounding(self, data):
        if data.get("message", '') == "permission granted":
            self.inbound = True
            return data
        else:
            return False

    def permission_to_aproach(self):
        return {"data": "ask"}

    def send_permission_to_inbound(self):
        flight = self.airplane_flight
        return {"data": "inbound_request",
                "coordinates": {"x": round(flight.x, 0), "y": round(flight.y, 0), "z": round(flight.z, 0)}}

    def send_landed_information(self):
        return {"data": "landed"}
