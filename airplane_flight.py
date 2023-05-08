import numpy as np
import random
import math
import logging


class AirplaneFlight:
    def __init__(self, uniqueId, x, y, z, velocity, fuel, airplane_instance):
        self.uniqueId = uniqueId
        self.x = x
        self.y = y
        self.z = z
        self.velocity = velocity
        self.fuel = fuel
        self.landed = False
        self.airplane_instance = airplane_instance

    def calculate_distance(self, x, y, z):
        return np.linalg.norm(np.array([self.x, self.y, self.z]) - np.array([x, y, z]))

    def update_position(self, direction_vector):
        self.x += self.velocity * direction_vector[0]
        self.x = round(self.x, 0)
        self.y += self.velocity * direction_vector[1]
        self.y = round(self.y, 0)
        self.z += self.velocity * direction_vector[2]
        self.z = round(self.z, 0)

    def get_airplane_data(self):
        return {
            'airplane_ID': self.uniqueId,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'velocity': self.velocity,
            'fuel': self.fuel
        }

    def update_airplane_position(self, corridor_x, corridor_y, corridor_z, distance):
        direction_vector = (np.array([corridor_x, corridor_y, corridor_z]) - np.array(
            [self.x, self.y, self.z])) / distance

        if 1000 > distance > 300:
            self.velocity = 50 - 40 * (distance - 300) / 700
        elif 300 >= distance > 150:
            self.velocity = 15 - 10 * (distance - 150) / 150
        elif distance <= 150:
            self.velocity = 7 - 4 * distance / 150
        else:
            pass

        self.update_position(direction_vector)
        self.fuel -= 1
        if self.fuel == 0:
            logging.error(f"Airplane {self.uniqueId} has run out of fuel and has collide")

    def fly_randomly(self):
        direction = random.randint(0, 360)
        self.x += self.velocity * math.cos(direction)
        self.x = round(self.x, 0)
        self.y += self.velocity * math.sin(direction)
        self.y = round(self.y, 0)
        self.z += self.velocity * math.sin(direction)
        self.z = round(self.z, 0)
        airplane_data = self.get_airplane_data()
        return {"data": "execute_approach", **airplane_data}

    def fly_to_corridor(self, corridor_x, corridor_y, corridor_z):
        distance = self.calculate_distance(corridor_x, corridor_y, corridor_z)
        airplane_data = self.get_airplane_data()
        logging.info(f"Airplane {self.uniqueId} is {round(distance, 0)} meters away from the corridor")
        if distance <= 100:
            self.handle_entered_corridor()
            landed_information = self.airplane_instance.send_landed_information()
            return {"airplane_ID": self.uniqueId, "x_coordinates": corridor_x, **landed_information, **airplane_data}
        else:
            self.update_airplane_position(corridor_x, corridor_y, corridor_z, distance)
            return {"data": "execute_runway_approach", **airplane_data}

    def handle_entered_corridor(self):
        logging.info(f"Airplane {self.uniqueId} has entered the corridor")
        self.landed = True
