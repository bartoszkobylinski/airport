import json
import threading
import math
from main_new import IP_PORT
from socket_connection import Socket_Connection


class Airport(Socket_Connection):

    airplanes = []
    lock = threading.Lock()

    def __init__(self):#, host='127.0.0.1', port=5000 , encoder='utf-8', buffer=2048):
        #self.host = host
        #self.port = port
        #self.encoder = encoder
        #self.buffer = buffer
        super().__init__()
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)
        self.runway1 = []
        self.runway2 = []
        self.x = 0
        self.y = 0
        self.z = 0
        self.corridor_1_x = 1000
        self.corridor_1_y = 2000
        self.corridor_1_z = 0
        self.corridor_2_x = -1000
        self.corridor_2_y = -2000
        self.corridor_2_z = 0

        

    def send_json(self, client_socket, data):
        json_data = json.dumps(data)
        client_socket.send(json_data.encode(self.encoder))
    
    def recv_json(self,client_socket):
        data= client_socket.recv(self.buffer)
        if not data: 
            return None
        json_data = json.loads(data.decode(self.encoder))
        return json_data

    def handle_new_client(self, client_socket):

        while True:
            data = self.recv_json(client_socket)
            print(f"I've got data: {data}")
            
            match data.get('data',''):
                case "ask":
                    print("Airport got question about permission to land")
                    message = self.give_permission_to_approach()
                    print(f"Message to airplane permission is: {message}")
                    self.send_json(client_socket, message)
                case "fly":
                    airplane_ID = data.get("airplane_ID",'')
                    x = data.get("coordinates",'').get("x",'')
                    y = data.get("coordinates",'').get("y",'')
                    z = data.get("coordinates",'').get("z",'')
                    airplane = dict()
                    airplane.update(airplane_ID=airplane_ID, x=x, y=y, z=z)
                    self.add_or_update_airplane_to_list(airplane_data=airplane)
                    self.check_all_collision(self.airplanes)
                    response = {"message":"ok"}
                    self.send_json(client_socket,response)
                case "inbound":
                    response =self.inbound_for_landing(data)
                    print(f"This is what I can tell about INBOUND: {response}")
                    self.send_json(client_socket, response)
                    airplane_ID = data.get("airplane_ID",'')
                    print(f"This is your DATA MF: {data.get('coordinates','')}")
                    x = data.get("coordinates",'').get("x",'')
                    y = data.get("coordinates",'').get("y",'')
                    z = data.get("coordinates",'').get("z",'')
                    airplane = dict()
                    airplane.update(airplane_ID=airplane_ID, x=x, y=y, z=z)
                    print(f"I have updated info about plane: {airplane.get('airplane_ID','')} x:{airplane.get('x','')} y: {airplane.get('y','')} z:{airplane.get('z','')}")
                    self.add_or_update_airplane_to_list(airplane_data=airplane)
                    response = {"message":"ok for inbounding"}
                    self.check_all_collision(self.airplanes)
                    self.send_json(client_socket, response)
                    print(response)
                case _:
                    print("Airplane send message with no case statement")
                    response = {"message": "Response: message recived"}
                    self.send_json(client_socket, response)
            """
                case "stop":
                    self.socket.close()
                    break
                case "inbound":
                    airplane_ID = data.get("airplane_ID",'')
                    print(f"This is your DATA MF: {data.get('coordinates','')}")
                    x = data.get("coordinates",'').get("x",'')
                    y = data.get("coordinates",'').get("y",'')
                    z = data.get("coordinates",'').get("z",'')
                    airplane = dict()
                    airplane.update(airplane_ID=airplane_ID, x=x, y=y, z=z)
                    print(f"I have updated info about plane: {airplane.get('airplane_ID','')} x:{airplane.get('x','')} y: {airplane.get('y','')} z:{airplane.get('z','')}")
                    self.add_or_update_airplane_to_list(airplane_data=airplane)
                    response = {"message":"ok for inbounding"}
                    self.check_all_collision(self.airplanes)
                    self.send_json(client_socket, response)
                case "fly":
                    airplane_ID = data.get("airplane_ID",'')
                    x = data.get("coordinates",'').get("x",'')
                    y = data.get("coordinates",'').get("y",'')
                    z = data.get("coordinates",'').get("z",'')
                    airplane = dict()
                    airplane.update(airplane_ID=airplane_ID, x=x, y=y, z=z)
                    self.add_or_update_airplane_to_list(airplane_data=airplane)
                    self.check_all_collision(self.airplanes)
                    response = {"message":"ok"}
                    self.send_json(client_socket,response)
                    
                case "nudy":
                    response = {"message":"bla bla bla"}
                    self.send_json(client_socket, response)
                case "print":
                    print(f"THIS IS A LIST OF AIRPLANES: {self.airplanes}")

                
            """
    def give_permission_to_approach(self):
        if len(self.airplanes) < 100:
            return {"message": True}
        else:
            return {"message": False}
    
    def inbound_for_landing(self, airplane_data):
        with self.lock:
            if len(self.runway1) != 0 and len(self.runway2) != 0:
                return {"message":"permission denied"}
            else:
                print(f"Flight number: {airplane_data.get('airplane_ID','')} approaching airports runway")
                if not self.runway1:
                    self.runway1.append(airplane_data)
                    return {'message':"permission granted", "data":{"x": self.corridor_1_x, "y": self.corridor_1_y, "z": self.corridor_1_z}}
                else:
                    self.runway2.append(airplane_data)
                    return  {'message':"permission granted", "data":{"x": self.corridor_2_x, "y": self.corridor_2_y, "z": self.corridor_2_z}}
    
    def add_or_update_airplane_to_list(self, airplane_data):
        with self.lock:
            airplane_ID = airplane_data.get("airplane_ID",'')
            found = False
            if len(self.airplanes) > 0:
                for plane in self.airplanes:
                    if airplane_ID == plane.get("airplane_ID"):
                        plane.update(airplane_data)
                        found = True
                        break
                if not found:
                    self.airplanes.append(airplane_data)
            else:
                self.airplanes.append(airplane_data)
    
    def check_collision(self, airplane1, airplane2, limit=10):
        x1, y1 = airplane1.get("x"), airplane1.get("y")
        x2, y2 = airplane2.get("x"), airplane2.get("y")
        distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        if distance < limit:
            return True
        else:
            return False
    
    def check_all_collision(self, airplanes, limit=10):
        for i in range(len(airplanes)):
            for j in range(i+1, len(airplanes)):
                if self.check_collision(airplanes[i], airplanes[j], limit=limit):
                    print("Airplanes collide")
                    return {"message": f"Airplanes {airplanes[i]} and {airplanes[j]} collide!"}
                else:
                    continue
        
        




airport = Airport()
lock = threading.Lock()

while True:
    print("Waititng for the incoming connections")
    print("-------------------------------------")
    try:
        client_socket, adrres = airport.socket.accept()
    except Exception as e:
        print(f"Server closed connection")
        break
    try:
        t = threading.Thread(target=airport.handle_new_client, args=[client_socket])
        t.start()
    except Exception as e:
        print(f"I try start new thread but i got Excpetion: {e}")
