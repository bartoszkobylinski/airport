import unittest
import json
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from socket_connection import SocketConnection


class TestSocketConnection(unittest.TestCase):

    def setUp(self):
        self.socket_connection = SocketConnection()

    def test_send_json(self):
        self.socket_connection.socket = MagicMock()
        test_data = {"key": "value"}
        self.socket_connection.send_json(test_data)
        self.socket_connection.sendall().assert_called()


    def test_recv_json(self):
        self.socket_connection.socket = MagicMock()
        test_data = {"key": "value"}
        json_data = json.dumps(test_data).encode()
        self.socket_connection.socket.recv.side_effect = [len(json_data).to_bytes(4, 'big'), json_data]
        received_data = self.socket_connection.recv_json()
        self.assertEqual(test_data, received_data)


if __name__ == "__main__":
    unittest.main()
