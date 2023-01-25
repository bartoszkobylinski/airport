import socket

class Socket_Connection(socket.socket):

    def __init__ (self, host='127.0.0.1', port=34000, encoder='utf-8', buffer=2048):
        self.host = host
        self.port = port
        self.encoder = encoder
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)