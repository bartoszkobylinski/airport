import numpy as np
import random
import math
import logging

from airplane.airplane_enums import Status


class AirplaneFlight:
    def __init__(self, uniqueId, x, y, z, velocity, fuel, airplane_instance):
        self.uniqueId = uniqueId
        self.x = x
        self.y = y
        self.z = z
        self.velocity = velocity
        self.fuel = fuel
        self.fuel_usage = random.randint(3, 7)
        self.landed = False
        self.runway_coordinates = None
        self.airplane_instance = airplane_instance

    def calculate_distance(self, x, y, z):
        return np.linalg.norm(np.array([self.x, self.y, self.z]) - np.array([x, y, z]))

    def get_airplane_data(self):
        return {
            'airplane_ID': self.uniqueId,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'velocity': self.velocity,
            'fuel': self.fuel,
            'status': self.airplane_instance.status.name
        }

    def update_airplane_position(self, direction_vector, distance=None):
        if distance is not None:
            if 1000 > distance > 300:
                self.velocity = 50 - 40 * (distance - 300) / 700
            elif 300 >= distance > 150:
                self.velocity = 15 - 10 * (distance - 150) / 150
            elif distance <= 150:
                self.velocity = 7 - 4 * distance / 150

        self.x += self.velocity * direction_vector[0]
        self.x = round(self.x, 0)
        self.y += self.velocity * direction_vector[1]
        self.y = round(self.y, 0)
        self.z += self.velocity * direction_vector[2]
        self.z = round(self.z, 0)
        self.fuel -= self.fuel_usage
        if self.fuel <= 0:
            logging.error(f"Airplane {self.uniqueId} has run out of fuel and has collided")
            print(f"Airplane: {self.uniqueId} collided")
            self.airplane_instance.status = Status.CRASHED
            print(self.airplane_instance.status.name)

    def handle_entered_corridor(self):
        self.landed = True
        self.airplane_instance.status = Status.LANDED

    def calculate_direction_vector(self, target_x, target_y, target_z):
        if target_x is None or target_y is None or target_z is None:
            # Generate a random direction
            direction = random.randint(0, 360)
            direction_vector = np.array([math.cos(direction), math.sin(direction), math.sin(direction)])
        else:
            # Calculate the direction vector towards the target
            direction_vector = (np.array([target_x, target_y, target_z]) - np.array([self.x, self.y, self.z]))
            direction_vector /= np.linalg.norm(direction_vector)
        return direction_vector

    def fly(self, target_x=None, target_y=None, target_z=None):
        direction_vector = self.calculate_direction_vector(target_x, target_y, target_z)
        if target_x is not None and target_y is not None and target_z is not None:
            distance = self.calculate_distance(target_x, target_y, target_z)
            print(f"Airplane {self.uniqueId} is {round(distance, 0)} meters away from the target. Fuel level: {self.fuel}")
            if distance <= 100:
                self.handle_entered_corridor()
                landed_information = self.airplane_instance.send_landed_information()
                return {"airplane_ID": self.uniqueId, "x_coordinates": target_x, **landed_information,
                        **self.get_airplane_data()}
            else:
                self.update_airplane_position(direction_vector, distance)
                return {"data": "execute_runway_approach", **self.get_airplane_data()}
        else:
            print(f"Airplane: {self.uniqueId}: flying randomly")
            self.update_airplane_position(direction_vector)
            return {"data": "execute_approach", **self.get_airplane_data()}

    def handle_collision(self, data):
        if data.get("airport_message", '') == "collision!":
            print(f"its a colisiosn")
            self.airplane_instance.status = Status.CRASHED
        else:
            print(data.get("airport_message", ''))
