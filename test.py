import unittest

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
    pass
    

if __name__ == "__main__":
    unittest.main()