import socket 
import json
import random
import string
import math
import time


class Airplane(socket.socket):
    unique_ids = set()

    def __init__ (self, host='127.0.0.1', port=9485, encoder='utf-8', buffer=2048):
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
        json_data = json.dumps(data_to_send)
        self.socket.send(json_data.encode(self.encoder))
        
    def recv_json(self):
            data = self.socket.recv(self.buffer)
            if data:
                json_data = json.loads(data.decode(self.encoder))
                return json_data
            else:
                self.socket.close()

    def fly_to_corridor(self, corridor_x, corridor_y, threshold = 50):
        self.set_direction_to_corridor(corridor_x, corridor_y)
        distance = math.sqrt((self.x - corridor_x)**2 + (self.y - corridor_y)**2)
        if distance >threshold:
            self.x += self.velocity * math.cos(self.direction)
            self.y += self.velocity * math.sin(self.direction)
            distance = math.sqrt((self.x - corridor_x)**2 + (self.y - corridor_y)**2)
            data = {"airplane_ID": self.uniqueID, 
                "data": {"x":self.x, "y":self.y,}}
                #"data":"dupa"}
            print(f"your distance is: {distance}")
            #self.send_json(data)
            print(f"I have send {data}")
            return data
        '''
        while distance > threshold:
            self.x += self.velocity * math.cos(self.direction)
            self.y += self.velocity * math.sin(self.direction)
            distance = math.sqrt((self.x - corridor_x)**2 + (self.y - corridor_y)**2)
            data = {"airplane_ID": self.uniqueID, 
                "data": {"x":self.x, "y":self.y,"velocity":self.velocity, "direction": self.direction}}
            print(f"your distance is: {distance}")
            self.send_json(data)
            time.sleep(1)
        '''

    def set_direction_to_corridor(self, corridor_x, corridor_y):
        self.direction = math.atan2(corridor_y - self.y, corridor_x - self.x)

    def recieve_permission(data):
        if data:
            return True
        else:
            del self
        
    def send_permission_to_aproach(self):
        return "ask"
        pass

airplane = Airplane()
airplane.send_json(airplane.send_permission_to_aproach())
msg = airplane.recieve_permission()
print(f"Airplane got message: {msg} so it can starting landing procedure")
time.sleep(3)

while msg:
    msg_1 = airplane.recv_json()
    print(f"I've got message from airport: {msg_1}")
    message = airplane.fly_to_corridor(0,0)
    airplane.send_json(message)
    time.sleep(3)
else:
    del airplane
