import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from reserved.airport_class import Airport


class TestAirport(unittest.TestCase):

    def setUp(self):
        self.airport = Airport()

    def tearDown(self):
        self.airport.socket.close()

    def test_request_landing_permission(self):
        action = "request_landing_permission"
        data = {}
        response = self.airport.process_action(action, data)
        self.assertIn("airport_message", response)

    def test_execute_approach(self):
        action = "execute_approach"
        data = {"airplane_ID": "A1", "x": 100, "y": 200, "z": 0}
        response = self.airport.process_action(action, data)
        self.assertIn("message", response)

    def test_request_runway_permission(self):
        action = "request_runway_permission"
        data = {"airplane_ID": "A1", "x": 100, "y": 200, "z": 0}
        response = self.airport.process_action(action, data)
        self.assertIn("message", response)

    def test_execute_runway_approach(self):
        action = "execute_runway_approach"
        data = {"airplane_ID": "A1", "x": 100, "y": 200, "z": 0}
        response = self.airport.process_action(action, data)
        self.assertIn("message", response)

    def test_confirm_landing(self):
        action = "confirm_landing"
        data = {"airplane_ID": "A1", "x_coordinates": 100}
        response = self.airport.process_action(action, data)
        self.assertIn("message", response)

    def test_unknown_action(self):
        action = "unknown_action"
        data = {"airplane_ID": "A1", "x": 100, "y": 200, "z": 0}
        response = self.airport.process_action(action, data)
        self.assertIn("message", response)


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
        self.assertEqual(len(self.airport.airplanes), 6)

    def test_grant_approach_permission(self):
        # Test when there are less than 100 airplanes
        self.airport.airplanes = [i for i in range(99)]
        result1 = self.airport.grant_approach_permission()
        self.assertEqual(result1, {"airport_message": "Permission to approach airport_class granted"})

        # Test when there are exactly 100 airplanes
        self.airport.airplanes = [i for i in range(100)]
        result2 = self.airport.grant_approach_permission()
        self.assertEqual(result2, {"airport_class message": "Permission to approach airport_class denied."})

        # Test when there are more than 100 airplanes
        self.airport.airplanes = [i for i in range(101)]
        result3 = self.airport.grant_approach_permission()
        self.assertEqual(result3, {"airport_class message": "Permission to approach airport_class denied."})

    def test_process_landing_permission_request(self):
        with patch("airport_class.logger") as mock_logger:
            # Test when there are less than 100 airplanes
            self.airport.airplanes = [i for i in range(99)]
            result1 = self.airport.process_landing_permission_request()
            self.assertEqual(result1, {"airport_message": "Permission to approach airport_class granted"})
            mock_logger.info.assert_called_with("Airport Control Tower: Received request for landing permission.")
            mock_logger.debug.assert_called_with(
                "Airport Control Tower: Response to airplane_class is: {'airport_message': 'Permission to approach airport_class granted'}")

            # Test when there are 100 or more airplanes
            self.airport.airplanes = [i for i in range(100)]
            result2 = self.airport.process_landing_permission_request()
            self.assertEqual(result2, {"airport_class message": "Permission to approach airport_class denied."})
            mock_logger.info.assert_called_with("Airport Control Tower: Received request for landing permission.")
            mock_logger.debug.assert_called_with(
                "Airport Control Tower: Response to airplane_class is: {'airport_class message': 'Permission to approach airport_class denied.'}")

    def test_add_or_update_airplane_to_list(self):
        airplane1 = {"airplane_ID": "plane1", "x": 1, "y": 2}
        self.airport.add_or_update_airplane_to_list(airplane1)
        self.assertEqual(self.airport.airplanes, [airplane1])

        airplane2 = {"airplane_ID": "plane2", "x": 3, "y": 4}
        self.airport.add_or_update_airplane_to_list(airplane2)
        self.assertEqual(self.airport.airplanes, [airplane1, airplane2])

        updated_airplane1 = {"airplane_ID": "plane1", "x": 5, "y": 6}
        self.airport.add_or_update_airplane_to_list(updated_airplane1)
        self.assertEqual(self.airport.airplanes, [updated_airplane1, airplane2])

        updated_airplane2 = {"airplane_ID": "plane2", "x": 7, "y": 8}
        self.airport.add_or_update_airplane_to_list(updated_airplane2)
        self.assertEqual(self.airport.airplanes, [updated_airplane1, updated_airplane2])

        airplane3 = {"airplane_ID": "plane3", "x": 9, "y": 10}
        self.airport.add_or_update_airplane_to_list(airplane3)
        self.assertEqual(self.airport.airplanes, [updated_airplane1, updated_airplane2, airplane3])

    def test_check_collision(self):
        airplane1 = {"airplane_ID": "plane1", "x": 0, "y": 0}
        airplane2 = {"airplane_ID": "plane2", "x": 5, "y": 5}
        airplane3 = {"airplane_ID": "plane3", "x": 5, "y": 15}


        # Test when two airplanes are too far away to collide
        result1 = self.airport.check_collision(airplane1, airplane3)
        self.assertEqual(result1, False)

        # Test when two airplanes are too close to collide
        result2 = self.airport.check_collision(airplane1, airplane2)
        self.assertEqual(result2, True)

        # Test when two airplanes are exactly at the collision limit
        result3 = self.airport.check_collision(airplane2, airplane3)
        self.assertEqual(result3, True)

        # Test when the distance is exactly equal to the limit
        result4 = self.airport.check_collision(airplane1, airplane3, limit=5.0)
        self.assertEqual(result4, False)

    def test_check_all_collision(self):
        airplanes = [
            {"airplane_ID": "plane1", "x": 0, "y": 0},
            {"airplane_ID": "plane2", "x": 5, "y": 5},
            {"airplane_ID": "plane3", "x": 5, "y": 15}
        ]

        # Test when there is a collision
        result1 = self.airport.check_all_collision(airplanes, limit=10)
        self.assertIn("collision!", result1["message"])

        # Test when there is no collision
        result2 = self.airport.check_all_collision(airplanes, limit=4)
        self.assertIn("No collision detected", result2["message"])

    def test_fly_valid_data(self):
        airplane_data = {
            "airplane_ID": "A123",
            "x": 10000,
            "y": 20000,
            "z": 30000
        }
        another_airplane_data = {
            "airplane_ID": "A234",
            "x": 400,
            "y": 2500,
            "z": 400
        }
        self.airport.airplanes.append(airplane_data)
        self.airport.airplanes.append(another_airplane_data)
        response = self.airport.fly(airplane_data)
        airplane = [plane for plane in self.airport.airplanes if plane["airplane_ID"] == "A123"][0]
        self.assertEqual(airplane["airplane_ID"], "A123")
        self.assertEqual(airplane["x"], 10000)
        self.assertEqual(airplane["y"], 20000)
        self.assertEqual(airplane["z"], 30000)
        print(response)
        self.assertEqual(response["message"], "No collision detected")

    def test_handle_inbound_request(self):
        # Test when both runways are free
        response1 = self.airport.handle_inbound_request({})
        self.assertEqual(response1["message"], "permission granted")
        self.assertIn("coordinates", response1)

        # Test when runway1 is occupied
        response2 = self.airport.handle_inbound_request({})
        self.assertEqual(response2["message"], "permission granted")
        self.assertIn("coordinates", response2)
        self.assertNotEqual(response1["coordinates"], response2["coordinates"])

        # Test when both runways are occupied
        self.airport.runway1 = True
        self.airport.runway2 = True
        response3 = self.airport.handle_inbound_request({})
        self.assertEqual(response3["message"], "permission denied")
        self.assertIn("data", response3)
        self.assertIn("1", response3["data"])
        self.assertIn("2", response3["data"])

        # Test when runway2 is free
        self.airport.runway1 = True
        self.airport.runway2 = False
        response4 = self.airport.handle_inbound_request({})
        self.assertEqual(response4["message"], "permission granted")
        self.assertIn("coordinates", response4)
        self.assertNotEqual(response4["coordinates"], response1["coordinates"])
        self.assertEqual(response4["coordinates"], response2["coordinates"])

    def test_handle_inbound(self):
        # Test with valid data
        airplane1 = {"airplane_ID": "plane1", "x": 1, "y": 2, "z": 3}
        response1 = self.airport.inbounding(airplane1)
        print("response1:", response1)
        self.assertEqual(response1["message"], "ok for inbounding")
        self.assertIn(airplane1, self.airport.airplanes)

        # Test with an update to the same airplane_class
        updated_airplane1 = {"airplane_ID": "plane1", "x": 4, "y": 5, "z": 6}
        response2 = self.airport.inbounding(updated_airplane1)
        self.assertEqual(response2["message"], "ok for inbounding")
        self.assertIn(updated_airplane1, self.airport.airplanes)
        self.assertNotIn(airplane1, self.airport.airplanes)

        # Test with another airplane_class (no collision)
        airplane2 = {"airplane_ID": "plane2", "x": 20, "y": 8, "z": 9}
        response3 = self.airport.inbounding(airplane2)
        self.assertEqual(response3["message"], "ok for inbounding")
        self.assertIn(airplane2, self.airport.airplanes)

        # Test with another airplane_class (collision)
        airplane3 = {"airplane_ID": "plane3", "x": 5, "y": 6, "z": 7}
        response4 = self.airport.inbounding(airplane3)
        print("response4", response4)
        self.assertEqual(response4["message"], "collision!")
        self.assertIn("airplane_class-1", response4)
        self.assertIn("airplane_class-2", response4)
        self.assertEqual(response4["airplane_class-1"]["airplane_ID"], "plane1")
        self.assertEqual(response4["airplane_class-2"]["airplane_ID"], "plane3")

    def clean_up(self):
        if self.airport.socket:
            self.airport.socket.close()

    def addCleanup(self, function, *args, **kwargs):
        self.addCleanup(self.clean_up())


if __name__ == "__main__":
    unittest.main()
