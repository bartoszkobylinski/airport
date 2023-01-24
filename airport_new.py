import socket
import json
import threading
import time
from main_new import IP_PORT

class Airport(socket.socket):

    airplanes = []
    lock = threading.Lock()

    def __init__(self, host='127.0.0.1', port=12000 , encoder='utf-8', buffer=2048):
        self.host = host
        self.port = port
        self.encoder = encoder
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)
        self.landing_lanes = {'1':[], '2':[]}
        self.x = 0
        self.y = 0
        self.z = 0
        

    def send_json(self, client_socket, data):
        json_data = json.dumps(data)
        client_socket.send(json_data.encode(self.encoder))
    
    def recv_json(self,client_socket):
        data= client_socket.recv(self.buffer)
        if not data: 
            return None
        json_data = json.loads(data.decode(self.encoder))
        return json_data
    
    def airplane_data_handler(self, data):
        pass

    def handle_new_client(self, client_socket):

        while True:
            data = self.recv_json(client_socket)
            match data.get('data',''):
                case "ask":
                    print("Airport got question about permission to land")
                    message = self.give_permission_to_approach()
                    print(f"Message to airplane permission is: {message}")
                    self.send_json(client_socket, message)
                    print("message has been sent to airplane")
                case "stop":
                    self.socket.close()
                    break
                case "fly":
                    airplane_ID = data.get("airplane_ID",'')
                    x = data.get("coordinates",'').get("x",'')
                    y = data.get("coordinates",'').get("y",'')
                    airplane = dict()
                    airplane.update(airplane_ID=airplane_ID, x=x, y=y)
                    print(f"I have updated info about plane: {airplane.get('airplane_ID','')} x:{airplane.get('x','')} y: {airplane.get('y','')}")
                    self.add_or_update_airplane_to_list(airplane_data=airplane)
                    response = "ok"
                    self.send_json(client_socket, response)
                case "nudy":
                    response = "bla, bla bla"
                    self.send_json(client_socket, response)
                case "print":
                    print(f"THIS IS A LIST OF AIRPLANES: {self.airplanes}")

                case _:
                    print("Airplane send message with no case statement")
                    response = {"response": "Response: message recived"}
                    self.send_json(client_socket, response)
            
                
            #time.sleep(5)

    def give_permission_to_approach(self):
        if len(self.__class__.airplanes) < 100:
            return True
        else:
            return False
    
    def add_or_update_airplane_to_list(self, airplane_data):
        with self.lock:
            if len(self.airplanes) > 0:
                for plane in self.airplanes:
                    if airplane_data.get("airplane_ID") == plane.get("airplane_ID"):
                        print("znalazlem aktualizuje")
                        plane.update(airplane_data)
                    else:
                        print(f"nie znalazlem takiego samego numeru samolotu")
                        self.airplanes.append(airplane_data)
            else:
                self.airplanes.append(airplane_data)
        
        




airport = Airport()
lock = threading.Lock()

while True:
    print("waititng for the incoming connections")
    try:
        client_socket, adrres = airport.socket.accept()
    except Exception as e:
        print(f"Server closed connection")
        break
    try:
        t = threading.Thread(target=airport.handle_new_client, args=[client_socket])
        t.start()
        print(f"this is airplanes: {airport.airplanes}")
    except Exception as e:
        print(f"I try start new thread but i got Excpetion: {e}")
