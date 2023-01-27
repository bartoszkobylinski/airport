import json
import random
import string
import math
import time
import numpy as np
from main_new import IP_PORT
from socket_connection import Socket_Connection


class Airplane(Socket_Connection):
    unique_ids = set()

    def __init__ (self):# host='127.0.0.1', port=5000, encoder='utf-8', buffer=2048):
        #self.host = host
        #self.port = port
        #self.encoder = encoder
        #self.buffer = buffer
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super().__init__()
        
        self.socket.connect((self.host, self.port))
        self.x = random.randint(-5000, 5000)
        self.y = random.randint(-5000, 5000)
        self.z = random.randint(2000, 5000)
        self.velocity = random.randint(10, 100)
        self.direction = random.randint(0, 360)
        self.fuel = random.randint(0, 1000)
        self.uniqueID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while self.uniqueID in Airplane.unique_ids:
            self.uniqueID = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        Airplane.unique_ids.add(self.uniqueID)
        self.permission_granted = None
        self.inbound = None
        self.landed = False

    def send_json(self, data):
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
        self.x = round(self.x, 0)
        self.y += self.velocity * math.sin(direction)
        self.y = round((self.y + self.velocity * math.sin(direction)), 0)
        self.z += self.velocity * math.sin(direction)
        self.z = round(self.z, 0)
        data = {"data":"fly", "coordinates":{"x":self.x, "y":self.y, "z":self.z}}
        return data

    def fly_to_corridor(self, corridor_x, corridor_y, corridor_z, threshold = 50):
        self.set_direction_to_corridor(corridor_x, corridor_y, corridor_z)
        distance = math.sqrt((self.x - corridor_x)**2 + (self.y - corridor_y)**2 +(self.z - corridor_z)**2)
        if distance >threshold:
            self.x += self.velocity * math.cos(self.direction)
            self.y += self.velocity * math.sin(self.direction)
            self.z += self.velocity * math.cos(self.direction)
            distance = math.sqrt((self.x - corridor_x)**2 + (self.y - corridor_y)**2 +(self.z - corridor_z)**2)
            data = {"data": "fly_to_corridor", "coordinates": {"x":round(self.x,2), "y":round(self.y,2), "z":round(self.z,2)}}
            print(f"your distance to corridor is: {distance}")
            time.sleep(0.5)
            return data

    def set_direction_to_corridor(self, corridor_x, corridor_y, corridor_z):
        target_vector = [corridor_x - self.x, corridor_y - self.y, corridor_z - self.z]
        z_vector = [0, 0, 1]
        dot_product = target_vector[0]*z_vector[0] + target_vector[1]*z_vector[1] + target_vector[2]*z_vector[2]
        target_vector_magnitude = math.sqrt(target_vector[0]**2 + target_vector[1]**2 + target_vector[2]**2)
        z_vector_magnitude = math.sqrt(z_vector[0]**2 + z_vector[1]**2 + z_vector[2]**2)
        self.direction = math.acos(dot_product / (target_vector_magnitude * z_vector_magnitude))

    def fly_to_corridor_numpy(self, corridor_x, corridor_y, corridor_z):
        distance = np.linalg.norm(np.array([self.x, self.y, self.z])- np.array([corridor_x, corridor_y, corridor_z]))
        print(f"Airplane {self.uniqueID} is {distance} meters away from the corridor")
        time.sleep(1.5)
        if distance <=100:
            print(f"Airplane {self.uniqueID} has entered the corridor")
            data = {"data":"landed"}
            self.landed = True
            return data
        else:
            direction_vector = (np.array([corridor_x, corridor_y, corridor_z])- np.array([self.x, self.y, self.z])) / distance
            self.x += self.velocity * direction_vector[0]
            self.x = round(self.x,0)
            self.y += self.velocity * direction_vector[1]
            self.y = round(self.y, 0)
            self.z += self.velocity * direction_vector[2]
            self.z = round(self.z, 0)
            self.fuel -= 1
            data = {"data":"inbound","coordinates": {"x":self.x, "y":self.y, "z":self.z}}
            if self.fuel == 0:
                print(f"Airplane {self.uniqueID} has run out of fuel and has collide")
            return data

    def recieve_permission(self, data):
        if data:
            self.permission_granted = True
            return True
        else:
            del self
    
    def recieve_permisssion_for_inbounding(self, data):
        if data.get("message",'') == "permission granted":
            self.inbound = True
            return data
            #return True
        else:
            return False        
        
    def permission_to_aproach(self):
        return {"data":"ask"}
    
    def send_permission_to_inbound(self):
        return {"data":"inbound","coordinates":{"x":round(self.x,0), "y":round(self.y,0), "z": round(self.z, 0)}}
        

airplane = Airplane()

while True:

    permision_to_aproach = airplane.permission_to_aproach()
    airplane.send_json(permision_to_aproach)
    airplane.recieve_permission(airplane.recv_json().get("message",''))
    
    while airplane.permission_granted :
        message = airplane.fly_randomly()
        airplane.send_json(message)
        server_message = airplane.recv_json()
        print(f"Server has sendt me this: {server_message}")
        time.sleep(1)
        message = airplane.send_permission_to_inbound()
        print(f"I have send permission to inbound: {message}")
        airplane.send_json(message)
        server_message = airplane.recv_json()
        print(f"I have got messag fro server: {server_message}")
        cooridor_coordinates = airplane.recieve_permisssion_for_inbounding(server_message)
        print(cooridor_coordinates)
        while airplane.inbound:
            if airplane.landed:
                airplane.socket.close()
                break
            else:
                message = airplane.fly_to_corridor_numpy(cooridor_coordinates.get("data").get("x"), cooridor_coordinates.get("data").get("y"), cooridor_coordinates.get("data").get("z"))
                print(message)
                airplane.send_json(message)
        
        
    else:
        del airplane

    '''
    if airplane.permission_granted:
        message = airplane.fly_randomly()
        airplane.send_json(message)
        message = airplane.send_permission_to_inbound()
        airplane.send_json(message)

    elif server_message.get("message") == "Permission granted":
        x = server_message.get("data").get("x")
        y = server_message.get("data").get("y")
        z = server_message.get("data").get("z")
        message = airplane.fly_to_corridor(x,y,z)
        airplane.send_json(message)
    server_message = airplane.recv_json()
    


    airplane.send_json(airplane.send_permission_to_inbound())
    if msg_1:
        pass 
    message = airplane.fly_to_corridor(0,0,0)
    airplane.send_json(message)
    time.sleep(3)
    airplane.send_json({"data":"print"})
    '''
    #server_message = airplane.recv_json()


