import json
import random
import string
import math
import time
import numpy as np
from socket_connection import SocketConnection
import logging

logging.basicConfig(level=logging.INFO)

class Airplane(SocketConnection):
    unique_ids = set()

    def __init__(self):
        super().__init__()

        self.socket.connect((self.host, self.port))
        self.init_airplane_state()
        self.permission_granted = None
        self.inbound = None
        self.landed = False

    def init_airplane_state(self):
        self.x = random.randint(-5000, 5000)
        self.y = random.randint(-5000, 5000)
        self.z = random.randint(2000, 5000)
        self.velocity = random.randint(50, 500)
        self.direction = random.randint(0, 360)
        self.fuel = random.randint(0, 1000)
        self.uniqueID = self.generate_unique_id()

    def generate_unique_id(self):
        uniqueID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while uniqueID in Airplane.unique_ids:
            uniqueID = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        Airplane.unique_ids.add(uniqueID)
        return uniqueID

    def send_json(self, data, airplane_id=None):
        if airplane_id is None:
            airplane_id = self.uniqueID
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

    def fly_randomly(self):
        direction = random.randint(0, 360)
        self.x += self.velocity * math.cos(direction)
        self.x = round(self.x, 0)
        self.y += self.velocity * math.sin(direction)
        self.y = round((self.y + self.velocity * math.sin(direction)), 0)
        self.z += self.velocity * math.sin(direction)
        self.z = round(self.z, 0)
        data = {"data": "fly", "coordinates": {"x": self.x, "y": self.y, "z": self.z}}
        return data

    def fly_to_corridor_numpy(self, corridor_x, corridor_y, corridor_z):
        distance = self.calculate_distance(corridor_x, corridor_y, corridor_z)
        logging.info(f"Airplane {self.uniqueID} is {round(distance, 0)} meters away from the corridor")
        time.sleep(1.5)

        if distance <= 100:
            self.handle_entered_corridor()
            return self.send_landed_information()
        else:
            self.update_airplane_position(corridor_x, corridor_y, corridor_z, distance)
            return self.send_inbound_coordinates()

    def calculate_distance(self, x, y, z):
        return np.linalg.norm(np.array([self.x, self.y, self.z]) - np.array([x, y, z]))

    def handle_entered_corridor(self):
        logging.info(f"Airplane {self.uniqueID} has entered the corridor")
        self.landed = True

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
                logging.error(f"Airplane {self.uniqueID} has run out of fuel and has collide")

    def send_landed_information(self):
        return {"data": "landed", "coordinates": {"x": self.x, "y": self.y, "z": self.z}}

    def send_inbound_coordinates(self):
        return {"data": "inbound", "coordinates": {"x": self.x, "y": self.y, "z": self.z}}

    def recieve_permission(self, data):
        if data:
            self.permission_granted = True
            return True
        else:
            del self
    
    def recieve_permisssion_for_inbounding(self, data):
        if data.get("message", '') == "permission granted":
            self.inbound = True
            return data
        else:
            return False        
        
    def permission_to_aproach(self):
        return {"data":"ask"}
    
    def send_permission_to_inbound(self):
        return {"data":"inbound_request","coordinates":{"x":round(self.x,0), "y":round(self.y,0), "z": round(self.z, 0)}}

    def send_landed_information(self):
        return {"data":"landed"}
        
