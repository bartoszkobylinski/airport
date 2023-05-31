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
        self.fuel_usage = random.randint(30, 70)
        self.landed = False
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
            'permission': self.airplane_instance.permission_granted,
            'inbounding': self.airplane_instance.inbound
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
        print(f"fuel: {self.fuel}")
        if self.fuel <= 0:
            logging.error(f"Airplane {self.uniqueId} has run out of fuel and has collided")
            print(f"Airplane collided {self.uniqueId}")
            self.airplane_instance.socket.close()
        else:
            print(
                f"Airplane {self.uniqueId} is now at position: ({self.x}, {self.y}, {self.z} with fuel level: {self.fuel} and velocity: {self.velocity})")

    '''
    def fly_randomly(self):
        direction = random.randint(0, 360)
        self.x += self.velocity * math.cos(direction)
        self.x = round(self.x, 0)
        self.y += self.velocity * math.sin(direction)
        self.y = round(self.y, 0)
        self.z += self.velocity * math.sin(direction)
        self.z = round(self.z, 0)
        airplane_data = self.get_airplane_data()
        # logging.info(f"Airplane {self.uniqueId}: flies with status: {self.airplane_instance.permission_granted} and "
        # f"inbound: {self.airplane_instance.inbound}")
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
    '''

    def handle_entered_corridor(self):
        self.landed = True

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
            print(f"I got cooordinates and distance is: {distance}")
            print(f"Airplane {self.uniqueId} is {round(distance, 0)} meters away from the target")
            if distance <= 100:
                self.handle_entered_corridor()
                landed_information = self.airplane_instance.send_landed_information()
                return {"airplane_ID": self.uniqueId, "x_coordinates": target_x, **landed_information,
                        **self.get_airplane_data()}
            else:
                print(f"this is fuel level: {self.fuel}")
                self.update_airplane_position(direction_vector, distance)
                print(f"this fuel level should varies: {self.fuel} ")
                return {"data": "execute_runway_approach", **self.get_airplane_data()}
        else:
            self.update_airplane_position(direction_vector)
            print(f"flying randomly")
            return {"data": "execute_approach", **self.get_airplane_data()}
