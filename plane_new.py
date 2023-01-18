import socket 
import json


class Airplane(socket.socket):

    def __init__ (self, host='127.0.0.1', port=9485, encoder='utf-8', buffer=1024):
        self.host = host
        self.port = port
        self.encoder = encoder
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_json(self, data):
        json_data = json.dumps(data)
        self.socket.send(json_data.encode(self.encoder))
        
    def recv_json(self):
        data = self.socket.recv(self.buffer)
        json_data = json.loads(data.decode(self.encoder))
        return json_data
airplane = Airplane()

while True:
    msg = input("onetuh: ")
    airplane.send_json(msg)

    msg = airplane.recv_json()
    print(msg)
    
