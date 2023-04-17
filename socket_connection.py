import socket
import random


class SocketConnection(socket.socket):

    def __init__ (self, port=13452, host='127.0.0.1', encoder='utf-8', buffer=2048):
        self.host = host
        self.port = port
        self.encoder = encoder
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
