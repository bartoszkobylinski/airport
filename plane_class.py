import json
import random
import string
import math
import time
import numpy as np
from socket_connection import SocketConnection
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AirplaneFlight:
    def __init__(self, uniqueId, x, y, z, velocity, fuel, airplane_instance):
        self.uniqueId = uniqueId
        self.x = x
        self.y = y
        self.z = z
        self.velocity = velocity
        self.fuel = fuel
        self.landed = False
        self.airplane_instance = airplane_instance

    def calculate_distance(self, x, y, z):
        return np.linalg.norm(np.array([self.x, self.y, self.z]) - np.array([x, y, z]))

    def update_position(self, direction_vector):
        self.x += self.velocity * direction_vector[0]
        self.x = round(self.x, 0)
        self.y += self.velocity * direction_vector[1]
        self.y = round(self.y, 0)
        self.z += self.velocity * direction_vector[2]
        self.z = round(self.z, 0)

    def get_airplane_data(self):
        return {
            'airplane_ID': self.uniqueId,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'velocity': self.velocity,
            'fuel': self.fuel
        }

    def update_airplane_position(self, corridor_x, corridor_y, corridor_z, distance):
        direction_vector = (np.array([corridor_x, corridor_y, corridor_z]) - np.array(
            [self.x, self.y, self.z])) / distance

        if 1000 > distance > 300:
            self.velocity = 50 - 40 * (distance - 300) / 700
        elif 300 >= distance > 150:
            self.velocity = 15 - 10 * (distance - 150) / 150
        elif distance <= 150:
            self.velocity = 7 - 4 * distance / 150
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
        airplane_data = self.get_airplane_data()
        return {"data": "execute_approach", **airplane_data}

    def fly_to_corridor(self, corridor_x, corridor_y, corridor_z):
        distance = self.calculate_distance(corridor_x, corridor_y, corridor_z)
        airplane_data = self.get_airplane_data()
        logging.info(f"Airplane {self.uniqueId} is {round(distance, 0)} meters away from the corridor")
        if distance <= 100:
            self.handle_entered_corridor()
            landed_information = self.airplane_instance.send_landed_information()
            return {"airplane_ID": self.uniqueId, "x_coordinates": corridor_x, **landed_information, **airplane_data}
        else:
            self.update_airplane_position(corridor_x, corridor_y, corridor_z, distance)
            return {"data": "execute_runway_approach", **airplane_data}

    def handle_entered_corridor(self):
        logging.info(f"Airplane {self.uniqueId} has entered the corridor")
        self.landed = True


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
