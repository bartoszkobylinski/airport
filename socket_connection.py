import logging
import socket
import struct
import json
import time


class SocketConnection(socket.socket):

    def __init__(self, port=11452, host='127.0.0.1', encoder='utf-8', buffer=2048, socket_instance=None):
        super().__init__()
        self.host = host
        self.port = port
        self.encoder = encoder
        self.buffer = buffer
        if socket_instance is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = socket_instance

    def send_json(self, data, custom_socket=None, airplane_id=None):
        if custom_socket is None:
            custom_socket = self.socket
        if airplane_id is not None:
            data = {"airplane_ID": airplane_id} | data
        json_data = json.dumps(data).encode(self.encoder)
        length = struct.pack('>I', len(json_data))
        time.sleep(1)
        try:
            custom_socket.sendall(length)
            custom_socket.sendall(json_data)
        except BrokenPipeError:
            logging.error("The connection was closed by the other side")

    def recv_json(self, custom_socket=None):
        if custom_socket is None:
            custom_socket = self.socket

        try:
            length_data = self._recvall(custom_socket, 4)
            if length_data is None:
                return None
            length = struct.unpack('>I', length_data)[0]
            json_data = self._recvall(custom_socket, length)
            if json_data is None:
                return None
            data = json.loads(json_data.decode(self.encoder))
            return data
        except ConnectionResetError:
            logging.error("The connection was reset by the other side.")
            return None

    def _recvall(self, custom_socket, n):
        data = bytearray()
        while len(data) < n:
            packet = custom_socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
