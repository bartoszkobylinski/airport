import unittest
import numpy as np

import re
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airplane_class.plane_class import UniqueIDGenerator, AirplaneFlight


class TestUniqueIDGenerator(unittest.TestCase):

    def test_generate_unique_id_format(self):
        unique_id = UniqueIDGenerator.generate_unique_id()
        pattern = re.compile("^[A-Z0-9]{6}$")
        self.assertTrue(pattern.match(unique_id), f"Unique ID {unique_id} does not match the expected format")

    def test_generate_unique_id_uniqueness(self):
        ids_set = set()
        for _ in range(1000):
            unique_id = UniqueIDGenerator.generate_unique_id()
            self.assertNotIn(unique_id, ids_set, f"Unique ID {unique_id} is not unique")
            ids_set.add(unique_id)


class TestAirplaneFlight(unittest.TestCase):

    def setUp(self):
        self.airplane = AirplaneFlight("ABC123", 0, 0, 0, 10, 100)

    def test_calculate_distance(self):
        distance = self.airplane.calculate_distance(10, 0, 0)
        expected_distance = 10
        self.assertEqual(distance, expected_distance, f"Calculated distance {distance} is not equal to {expected_distance}")

    def test_update_position(self):
        direction_vector = np.array([1, 0, 0])
        self.airplane.update_position(direction_vector)
        expected_position = (10, 0, 0)
        self.assertEqual((self.airplane.x, self.airplane.y, self.airplane.z), expected_position, f"Updated position is not equal to {expected_position}")

    def test_fuel_depletion(self):
        initial_fuel = self.airplane.fuel
        direction_vector = np.array([1, 0, 0])
        self.airplane.update_position(direction_vector)
        self.assertEqual(self.airplane.fuel, initial_fuel - 1, "Fuel not depleted after updating position")

    def test_fly_randomly(self):
        initial_position = (self.airplane.x, self.airplane.y, self.airplane.z)
        result = self.airplane.fly_randomly()
        new_position = (self.airplane.x, self.airplane.y, self.airplane.z)
        self.assertNotEqual(initial_position, new_position, "Airplane position did not change after flying randomly")

    def test_fly_to_corridor(self):
        corridor_x, corridor_y, corridor_z = 1000, 0, 0
        result = self.airplane.fly_to_corridor(corridor_x, corridor_y, corridor_z)
        new_position = (self.airplane.x, self.airplane.y, self.airplane.z)
        distance = np.linalg.norm(np.array(new_position) - np.array([corridor_x, corridor_y, corridor_z]))
        self.assertLess(distance, 1000, "Airplane is not closer to the corridor after flying to it")

    def test_handle_entered_corridor(self):
        self.airplane.handle_entered_corridor()
        self.assertTrue(self.airplane.landed, "Airplane did not set landed flag to True after entering the corridor")

    def test_fuel_depletion(self):
        initial_fuel = self.airplane.fuel
        self.airplane.update_airplane_position(100, 100, 100, 1000)
        self.assertEqual(self.airplane.fuel, initial_fuel - 1, "Fuel not depleted after updating position")

    def test_velocity_decreases_with_distance(self):
        corridor_x = 1000
        corridor_y = 1000
        corridor_z = 1000
        for i in range(5):
            previous_distance = self.airplane.calculate_distance(corridor_x, corridor_y, corridor_z)
            previous_velocity = self.airplane.velocity
            self.airplane.update_airplane_position(corridor_x, corridor_y, corridor_z, previous_distance)
            new_distance = self.airplane.calculate_distance(corridor_x, corridor_y, corridor_z)
            new_velocity = self.airplane.velocity

            self.assertLessEqual(new_distance, previous_distance,
                                 f"New distance {new_distance} is not less than or equal to previous distance {previous_distance}")
            self.assertLessEqual(new_velocity, previous_velocity,
                                 f"Airplane velocity did not decrease or remain the same when distance decreased. "
                                 f"Previous distance: {previous_distance}, New distance: {new_distance}, "
                                 f"Previous velocity: {previous_velocity}, New velocity: {new_velocity}")





if __name__ == '__main__':
    unittest.main()