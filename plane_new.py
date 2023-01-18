import socket 


class Airplane(socket.socket):

    def __init__ (self, host='127.0.0.1', port=7485):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        
airplane = Airplane()

while True:
    msg = input("onetuh: ")
    airplane.socket.send(msg.encode())

    msg = airplane.socket.recv(1024)
    print(msg)
    
