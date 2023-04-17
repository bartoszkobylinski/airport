import unittest
import json
from unittest.mock import MagicMock, create_autospec

from airport_class import Airport
from socket_connection import Socket_Connection

class TestSocketConnection(unittest.TestCase):

    def test_instance_creation(self):
        connection = Socket_Connection()
        self.assertIsInstance(connection, Socket_Connection)
        self.assertEqual(connection.host, "127.0.0.1")
        self.assertEqual(connection.port, 33452)
        self.assertEqual(connection.encoder, "utf-8")
        self.assertEqual(connection.buffer, 2048)

class TetsAirport(unittest.TestCase):

    def setUp(self):
        self.airport = create_autospec(Airport)
        self.airport.socket = MagicMock()
        self.client_socket = MagicMock()
        self.data = {"key":"value"}

    def test_socket_connection(self):
        self.airport.socket.getsockname.return_value = ("127.0.0.1", 5000)
        self.assertEqual(self.airport.socket.getsockname(), ('127.0.0.1', 5000))
    
    def test_listen(self):
        result = self.airport.socket.listen()
        self.assertEqual(self.airport.socket.listen(), result)

    def test_initial_attributes(self):
        attributes = ['runway1','runway2','x','y','z','corridor_1_x', 'corridor_1_y','corridor_1_z',
        'corridor_2_x', 'corridor_2_y','corridor_2_z']
        for attribute in attributes:
            if hasattr(self.airport, attribute):
                self.assertFalse(getattr(self.airport, attribute))
            else:
                pass

    def test_send_json(self):
        self.airport.send_json(self.client_socket, self.data)
        self.client_socket.send.assert_called_once_with(json.dumps(self.data).encode(self.airport.encoder))

    def test_recv_json(self):
        self.client_socket.recv.return_value = json.dumps(self.data).encode(self.airport.encoder)
        result = self.airport.recv_json(self.client_socket)
        self.assertEqual(result, self.data)
    
    def test_give_permission_to_approach(self):
        self.airport.airplanes = []
        self.airport.give_permission_to_approach.return_value = {"message": True}
        result = self.airport.give_permission_to_approach()
        self.assertEqual(result, {"message": True})
        self.airport.airplanes = [x for x in range(110)]
        self.airport.give_permission_to_approach.return_value = {"message": False}
        result = self.airport.give_permission_to_approach()
        self.assertEqual(result, {"message": False})

    def test_inbound_for_landing(self):
        self.airport.lock = MagicMock()
        self.airport.inbound_for_landing.return_value = {'message': 'permission granted', 'data': {'x': 1, 'y': 2, 'z': 3}}

        with self.airport.lock:
            result1 = self.airport.inbound_for_landing()
        self.assertEqual(result1, {'message':"permission granted", "data":{"x": 1, "y": 2, "z": 3}})

        with self.airport.lock:
            result2 = self.airport.inbound_for_landing()
        self.assertEqual(result2, {'message':"permission granted", "data":{"x": 1, "y": 2, "z": 3}})

        with self.airport.lock:
            result3 = self.airport.inbound_for_landing()
        self.assertEqual(result3, {"message":"permission denied"})

if __name__ == "__main__":
    unittest.main()

