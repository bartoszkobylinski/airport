import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airplane.plane_class import Airplane, UniqueIDGenerator


class TestAirplane(Airplane):
    def __init__(self):
        super(Airplane, self).__init__()
        self.init_airplane_state()
        self.permission_granted = None
        self.inbound = None

class TestAirplaneMethods(unittest.TestCase):

    def setUp(self):
        self.mock_socket = MagicMock()
        self.airplane = Airplane(socket=self.mock_socket)


    def test_init_airplane_state(self):
        self.assertIsInstance(self.airplane.airplane_flight.uniqueId, str)
        self.assertIn(self.airplane.airplane_flight.uniqueId, UniqueIDGenerator.unique_ids)
        self.assertIsInstance(self.airplane.airplane_flight.x, int)
        self.assertIsInstance(self.airplane.airplane_flight.y, int)
        self.assertIsInstance(self.airplane.airplane_flight.z, int)
        self.assertIsInstance(self.airplane.airplane_flight.velocity, int)
        self.assertIsInstance(self.airplane.airplane_flight.fuel, int)
    def test_request_landing_permission(self):
        request = self.airplane.request_landing_permission()
        self.assertEqual(request, {"data": "request_landing_permission"})
    def test_receive_approach_permission(self):
        self.airplane.receive_approach_permission(True)
        self.assertTrue(self.airplane.permission_granted)
        self.airplane.permission_granted = False
        self.airplane.receive_approach_permission(False)
        self.assertFalse(self.airplane.permission_granted)
    def test_request_runway_permission(self):
        request = self.airplane.request_runway_permission()
        self.assertEqual(request, {"data": "request_runway_permission"})
    def test_grant_permission_for_inbounding(self):
        data = {"message": "permission granted"}
        response = self.airplane.grant_permission_for_inbounding(data)
        self.assertEqual(response, data)
        self.assertTrue(self.airplane.inbound)

        self.airplane.inbound = False
        data = {"message": "permission denied", "data": {"1": True, "2": True}}
        response = self.airplane.grant_permission_for_inbounding(data)
        self.assertFalse(response)
        self.assertFalse(self.airplane.inbound)
    def test_extract_runway_coordinates(self):
        data = {"coordinates": {"x": 100, "y": 200, "z": 300}}
        x, y, z = self.airplane.extract_runway_coordinates(data)
        self.assertEqual(x, 100)
        self.assertEqual(y, 200)
        self.assertEqual(z, 300)
    def test_send_landed_information(self):
        message = self.airplane.send_landed_information()
        self.assertEqual(message, {"data": "confirm_landing"})

    def test_unique_ids(self):
        airplane1 = Airplane(socket=self.mock_socket)
        self.assertNotEqual(self.airplane.airplane_flight.uniqueId, airplane1.airplane_flight.uniqueId)

    def test_del_self(self):
        airplane = Airplane(socket=self.mock_socket)
        airplane.receive_approach_permission(False)
        with self.assertRaises(NameError):
            airplane.permission_granted

    def test_coordinate_extraction_failure(self):
        data = {"coordinates": {"a": 1, "b": 2, "c": 3}}
        x, y, z = self.airplane.extract_runway_coordinates(data)
        self.assertEqual(x, '')
        self.assertEqual(y, '')
        self.assertEqual(z, '')


if __name__ == '__main__':
    unittest.main()
