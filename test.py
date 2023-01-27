import unittest
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

    def test_socket_connection(self):
        self.airport.socket = MagicMock()
        self.airport.socket.getsockname.return_value = ("127.0.0.1", 5000)
        self.assertEqual(self.airport.socket.getsockname(), ('127.0.0.1', 5000))
    
    def test_listen(self):
        self.airport.socket = MagicMock()
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

if __name__ == "__main__":
    unittest.main()

