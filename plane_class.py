import json
import random
import string
import math
import time
import numpy as np
from socket_connection import SocketConnection
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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

    def update_position(self, direction_vector):
        self.x += self.velocity * direction_vector[0]
        self.x = round(self.x, 0)
        self.y += self.velocity * direction_vector[1]
        self.y = round(self.y, 0)
        self.z += self.velocity * direction_vector[2]
        self.z = round(self.z, 0)

    def update_airplane_position(self, corridor_x, corridor_y, corridor_z, distance):
        direction_vector = (np.array([corridor_x, corridor_y, corridor_z]) - np.array(
            [self.x, self.y, self.z])) / distance

        if 1000 > distance > 300:
            self.velocity = random.randint(10, 50)
        elif 300 > distance > 150:
            self.velocity = random.randint(5, 15)
        elif distance < 150:
            self.velocity = random.randint(3, 7)
        else:
            pass

        self.update_position(direction_vector)
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
        return {"data": "execute_approach", "x": self.x, "y": self.y, "z": self.z}

    def fly_to_corridor(self, corridor_x, corridor_y, corridor_z):
        distance = self.calculate_distance(corridor_x, corridor_y, corridor_z)
        logging.info(f"Airplane {self.uniqueId} is {round(distance, 0)} meters away from the corridor")
        if distance <= 100:
            self.handle_entered_corridor()
            return {"airplane_ID": self. uniqueId, "x_coordinates": corridor_x}
        else:
            self.update_airplane_position(corridor_x, corridor_y, corridor_z, distance)
            return {"data": "execute_runway_approach", "x": self.x, "y": self.y, "z": self.z}

    def handle_entered_corridor(self):
        logging.info(f"Airplane {self.uniqueId} has entered the corridor")
        self.landed = True


class Airplane(SocketConnection):
    unique_ids = set()

    def __init__(self):
        super().__init__()

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
        self.airplane_flight = AirplaneFlight(uniqueID, x, y, z, velocity, fuel)
    def request_landing_permission(self):
        return {"data": "request_landing_permission"}
    def receive_approach_permission(self, data):
        if data:
            self.permission_granted = True
        else:
            del self
    def request_runway_permission(self):
        return {"data": "request_runway_permission"}

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
        return {"data": "confirm_landing"}
