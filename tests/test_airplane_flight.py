import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plane_class import Airplane
from airplane_flight import AirplaneFlight
from unique_generator import UniqueIDGenerator


class TestAirplaneFlightMethods(unittest.TestCase):
    def setUp(self):
        self.mock_airplane = MagicMock(spec=Airplane)
        self.mock_airplane.permission_granted = True
        self.mock_airplane.inbound = False
        self.airplane_flight = AirplaneFlight(
            uniqueId="123",
            x=0,
            y=0,
            z=0,
            velocity=10,
            fuel=100,
            airplane_instance=self.mock_airplane
        )

    def test_calculate_distance(self):
        distance = self.airplane_flight.calculate_distance(3, 4, 0)
        self.assertEqual(distance, 5)

    def test_update_position(self):
        self.airplane_flight.update_position([1, 1, 1])
        self.assertEqual(self.airplane_flight.x, 10)
        self.assertEqual(self.airplane_flight.y, 10)
        self.assertEqual(self.airplane_flight.z, 10)

    def test_get_airplane_data(self):
        data = self.airplane_flight.get_airplane_data()
        expected_data = {
            'airplane_ID': '123',
            'x': 0,
            'y': 0,
            'z': 0,
            'velocity': 10,
            'fuel': 100,
            'permission': self.mock_airplane.permission_granted,
            'inbounding': self.mock_airplane.inbound
        }
        self.assertEqual(data, expected_data)

    def test_fly_randomly(self):
        self.mock_airplane.permission_granted = True
        self.mock_airplane.inbound = False
        data = self.airplane_flight.fly_randomly()
        self.assertIn('data', data)
        self.assertIn('execute_approach', data['data'])

    def test_fly_to_corridor(self):
        self.mock_airplane.permission_granted = True
        self.mock_airplane.inbound = False
        data = self.airplane_flight.fly_to_corridor(10000, 10000, 10000)
        self.assertIn('data', data)
        self.assertIn('execute_runway_approach', data['data'])

    def test_handle_entered_corridor(self):
        self.airplane_flight.handle_entered_corridor()
        self.assertTrue(self.airplane_flight.landed)

    def test_update_airplane_position_with_fuel_consumption(self):
        self.airplane_flight.update_airplane_position(10, 10, 10, 50)
        self.assertEqual(self.airplane_flight.fuel, 97)
        self.assertNotEqual(self.airplane_flight.x, 0)
        self.assertNotEqual(self.airplane_flight.y, 0)
        self.assertNotEqual(self.airplane_flight.z, 0)

    def test_fly_to_corridor_when_airplane_is_less_then_100(self):
        self.mock_airplane.send_landed_information = MagicMock(return_value={"landed": True})
        self.airplane_flight.calculate_distance = MagicMock(return_value=90)
        data = self.airplane_flight.fly_to_corridor(100, 100, 100)
        self.assertEqual(data["airplane_ID"], "123")
        self.assertEqual(data["x_coordinates"], 100)
        self.assertEqual(data["landed"], True)


if __name__ == '__main__':
    unittest.main()
