import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airport_class import Airport


class TestAirport(unittest.TestCase):

    def setUp(self):
        self.airport = Airport()

    def tearDown(self):
        self.airport.socket.close()

    def test_process_action(self):
        # Test the process_action method with different action strings
        result = self.airport.process_action("request_landing_permission", {})
        self.assertIn("airport_message", result)

        result = self.airport.process_action("execute_approach", {})
        self.assertIn("message", result)

        result = self.airport.process_action("request_runway_permission", {})
        self.assertIn("message", result)

        result = self.airport.process_action("execute_runway_approach", {})
        self.assertIn("message", result)

        result = self.airport.process_action("confirm_landing", {"airplane_ID": "test_plane", "x_coordinates": 1000})
        self.assertIn("message", result)

        result = self.airport.process_action("unknown_action", {})
        self.assertIn("message", result)

    @patch('airport_class.Airport.recv_json', side_effect=[{"data": "request_landing_permission"}, None])
    def test_handle_new_client(self, recv_json_mock):
        client_socket_mock = MagicMock()
        self.airport.send_json = MagicMock()

        self.airport.handle_new_client(client_socket_mock)

        recv_json_mock.assert_called()
        self.airport.send_json.assert_called()

    def test_init_method(self):
        self.assertIsInstance(self.airport, Airport)
        self.assertEqual(self.airport.x, 0)
        self.assertEqual(self.airport.y, 0)
        self.assertEqual(self.airport.z, 0)
        self.assertEqual(self.airport.corridor_1_x, 1000)
        self.assertEqual(self.airport.corridor_1_y, 2000)
        self.assertEqual(self.airport.corridor_1_z, 0)
        self.assertEqual(self.airport.corridor_2_x, 4000)
        self.assertEqual(self.airport.corridor_2_y, 2000)
        self.assertEqual(self.airport.corridor_2_z, 0)
        self.assertFalse(self.airport.runway1)
        self.assertFalse(self.airport.runway2)
        self.assertIsInstance(self.airport.airplanes, list)
        self.assertEqual(len(self.airport.airplanes), 0)

    def test_grant_approach_permission(self):
        # Test when there are less than 100 airplanes
        self.airport.airplanes = [i for i in range(99)]
        result1 = self.airport.grant_approach_permission()
        self.assertEqual(result1, {"airport_message": "Permission to approach airport granted"})

        # Test when there are exactly 100 airplanes
        self.airport.airplanes = [i for i in range(100)]
        result2 = self.airport.grant_approach_permission()
        self.assertEqual(result2, {"airport message": "Permission to approach airport denied."})

        # Test when there are more than 100 airplanes
        self.airport.airplanes = [i for i in range(101)]
        result3 = self.airport.grant_approach_permission()
        self.assertEqual(result3, {"airport message": "Permission to approach airport denied."})

    def test_process_landing_permission_request(self):
        with patch("airport_class.logger") as mock_logger:
            # Test when there are less than 100 airplanes
            self.airport.airplanes = [i for i in range(99)]
            result1 = self.airport.process_landing_permission_request()
            self.assertEqual(result1, {"airport_message": "Permission to approach airport granted"})
            mock_logger.info.assert_called_with("Airport Control Tower: Received request for landing permission.")
            mock_logger.debug.assert_called_with(
                "Airport Control Tower: Response to airplane is: {'airport_message': 'Permission to approach airport granted'}")

            # Test when there are 100 or more airplanes
            self.airport.airplanes = [i for i in range(100)]
            result2 = self.airport.process_landing_permission_request()
            self.assertEqual(result2, {"airport message": "Permission to approach airport denied."})
            mock_logger.info.assert_called_with("Airport Control Tower: Received request for landing permission.")
            mock_logger.debug.assert_called_with(
                "Airport Control Tower: Response to airplane is: {'airport message': 'Permission to approach airport denied.'}")


if __name__ == "__main__":
    unittest.main()
