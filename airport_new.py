import socket
import json
import threading

class Airport(socket.socket):

    def __init__(self, host='127.0.0.1', port=9485 , encoder='utf-8', buffer=1024):
        self.host = host
        self.port = port
        self.encoder = encoder
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)
        self.landing_lanes = {'1':[], '2':[]}
        self.width = 10000
        self.long = 10000
        self.high = 5000

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
            print(f"{type(data)} and: {data}")
            match data:
                case "stop":
                    self.socket.close()
                case "time":
                    response = "to jest czas: bla"
                    self.send_json(client_socket, response)
                case "nudy":
                    response = "bla, bla bla"
                    self.send_json(client_socket, response)
                case _:
                    response = {"response": "Response: message recived"}
                    self.send_json(client_socket, response)

airport = Airport()


while True:
    print("waititng for the incoming connections")
    try:
        client_socket, adrres = airport.socket.accept()
    except Exception as e:
        print(f"there is e: {e}")
        break
    try:
        t = threading.Thread(target=airport.handle_new_client, args=[client_socket])
        t.start()
    except Exception as e:
        print(f"I try start new thread but i got Excpetion: {e}")
