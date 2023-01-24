import socket 
import json
import random
import string
import math
import time
from main_new import IP_PORT


class Airplane(socket.socket):
    unique_ids = set()

    def __init__ (self, host='127.0.0.1', port=12000, encoder='utf-8', buffer=2048):
        self.host = host
        self.port = port
        self.encoder = encoder
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.x = random.randint(-5000, 5000)
        self.y = random.randint(-5000, 5000)
        self.z = random.randint(2000, 5000)
        self.velocity = random.randint(10, 20)
        self.direction = random.randint(0, 360)
        self.fuel = random.randint(0, 1000)
        self.uniqueID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while self.uniqueID in Airplane.unique_ids:
            self.uniqueID = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        Airplane.unique_ids.add(self.uniqueID)

    def send_json(self, data):
        print(f"klient otrzymal: {data}")
        data_to_send = {"airplane_ID": self.uniqueID} | data
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
        self.y += self.velocity * math.sin(direction)
        self.z += self.velocity * math.sin(direction)
        data = {"data":"fly", "coordinates":{"x":round(self.x,2), "y":round(self.y, 2), "z":round(self.z,2)}}
        return data

    def fly_to_corridor(self, corridor_x, corridor_y, corridor_z, threshold = 50):
        self.set_direction_to_corridor(corridor_x, corridor_y, corridor_z)
        distance = math.sqrt((self.x - corridor_x)**2 + (self.y - corridor_y)**2 +(self.z - corridor_z)**2)
        if distance >threshold:
            self.x += self.velocity * math.cos(self.direction)
            self.y += self.velocity * math.sin(self.direction)
            self.z += self.velocity * math.sin(self.direction)
            distance = math.sqrt((self.x - corridor_x)**2 + (self.y - corridor_y)**2 +(self.z - corridor_z)**2)
            data = {"data": "fly_to_corridor", "coordinates": {"x":round(self.x,2), "y":round(self.y,2), "z":round(self.z,2)}}
            print(f"your distance is: {distance}")
            print(f"I have send {data}")
            return data

    def set_direction_to_corridor(self, corridor_x, corridor_y, corridor_z):
        target_vector = [corridor_x - self.x, corridor_y - self.y, corridor_z - self.z]
        z_vector = [0, 0, 1]
        dot_product = target_vector[0]*z_vector[0] + target_vector[1]*z_vector[1] + target_vector[2]*z_vector[2]
        target_vector_magnitude = math.sqrt(target_vector[0]**2 + target_vector[1]**2 + target_vector[2]**2)
        z_vector_magnitude = math.sqrt(z_vector[0]**2 + z_vector[1]**2 + z_vector[2]**2)
        self.direction = math.acos(dot_product / (target_vector_magnitude * z_vector_magnitude))

    def recieve_permission(data):
        if data:
            return True
        else:
            del self
        
    def send_permission_to_aproach(self):
        return {"data":"ask"}
        

airplane = Airplane()
airplane.send_json(airplane.send_permission_to_aproach())
msg = airplane.recieve_permission()
time.sleep(3)

while msg:
    msg_1 = airplane.recv_json()
    print(f"I've got message from airport: {msg_1}")
    message = airplane.fly_randomly()
    message = airplane.fly_to_corridor(0,0,0)
    airplane.send_json(message)
    time.sleep(3)
    airplane.send_json({"data":"print"})
else:
    del airplane
