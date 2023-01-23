import socket 
import json
import random
import string
import math
import time


class Airplane(socket.socket):
    unique_ids = set()

    def __init__ (self, host='127.0.0.1', port=5485, encoder='utf-8', buffer=1024):
        self.host = host
        self.port = port
        self.encoder = encoder
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.x = random.randint(-5000, 5000)
        self.y = random.randint(-5000, 5000)
        self.velocity = random.randint(10, 20)
        self.direction = random.randint(0, 360)
        self.fuel = random.randint(0, 1000)
        self.uniqueID = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        while self.uniqueID in Airplane.unique_ids:
            self.uniqueID = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        Airplane.unique_ids.add(self.uniqueID)

    def send_json(self, data):
        data_to_send = {"airplane_ID": self.uniqueID,'data':data}
        #data_to_send[self.uniqueID] = dict()
        #data_to_send[self.uniqueID].update(data=data)
        json_data = json.dumps(data_to_send)
        self.socket.send(json_data.encode(self.encoder))
        
    def recv_json(self):
            data = self.socket.recv(self.buffer)
            if data:
                json_data = json.loads(data.decode(self.encoder))
                return json_data
            else:
                self.socket.close()

    def move(self):
        self.x += self.velocity * math.cos(self.direction)
        self.y += self.velocity * math.sin(self.direction)
        print(f"my position is x: {self.x} and {self.y}")
        data = {"airplane_ID": self.uniqueID, 
        "data": {"x":self.x, "y":self.y,"velocity":self.velocity, "direction": self.direction}}
        return data
    
    def recieve_permission(self):
        pass

    def check_corridor_approach(self, corridor_coordinates):
        x_corridor, y_corridor, z_corridor = corridor_coordinates
        distance = math.sqrt((self.x - x_corridor)**2 + (self.y - y_corridor)**2 +(self.z - z_corridor)**2)
        if distance < THRESHOLD_DISTANCE:
            self.velocity


airplane = Airplane()
'''
while True:
    msg = input("onetuh: ")
    airplane.send_json(msg)
    if not msg:
        airplane.close()
        break
    msg = airplane.recv_json()
    print(msg)
'''

while True:
    move = airplane.move()
    print(f"move data type: {type(move)} and move data: {move}")
    airplane.send_json(move)
    data = airplane.recv_json
    if data:
        print(data)
    
    time.sleep(1)
