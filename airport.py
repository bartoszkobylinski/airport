import socket as soc
import json


class Connection:
    
    def __init__(self, host='127.0.0.1', port=6470, buffer=1024, encoder='utf-8', connection_type="Airport"):
        self.host = host
        self.port = port
        self.buffer = buffer
        self.encoder = encoder
        self.connection_type = connection_type
        self.socket = None
        self.connection = None
        self.address = None

    def __enter__(self):
        if self.connection_type == "Airport":
            self.socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen()
            cli_soc,self.address = self.socket.accept()
            self.connection = cli_soc
        if self.connection_type == "Airplane":
            self.connection = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
            self.connection.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_val):
        self.connection.close()
        del self

    def send_json(self, data):
        package = json.dump(data, indent=2)
        self.connection.send(package.encode(self.encoder))

    def send_raw(self, data):
        self.connection.send(data.encode(self.encoder))
    
    def recv_data(self):
        return json.loads(self.connection.recv(self.buffer).decode(self.encoder))
    
    def __str__(self) -> str:
        if self.connection_type == "airport":
            return "Airport control tower is active"
        elif self.connection_type == "airplane":
            return "Airplane is actvie"
        else:
            return "Either airport nor airplane is active"

