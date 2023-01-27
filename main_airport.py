import random

IP_PORT = random.randint(5000, 20000)
'''
import numpy as np

class Airport(Socket_Connection):
    # existing code here

    def simulate_flight(self):
        while True:
            for airplane in Airport.airplanes:
                distance = np.linalg.norm(np.array(
                    [airplane.x, airplane.y, airplane.z]) 
                    - np.array([self.corridor_1_x, self.corridor_1_y, self.corridor_1_z]))
                print(f'Airplane {airplane.id} is {distance} meters away from the corridor.')
                if distance <= 100:
                    print(f'Airplane {airplane.id} has entered the corridor.')
                    Airport.airplanes.remove(airplane)
                else:
                    direction_vector = (np.array([self.corridor_1_x, self.corridor_1_y, self.corridor_1_z]) - 
                        np.array([airplane.x, airplane.y, airplane.z])) / distance
                    airplane.x += airplane.velocity * direction_vector[0]
                    airplane.y += airplane.velocity * direction_vector[1]
                    airplane.z += airplane.velocity * direction_vector[2]
                    airplane.fuel -= 1
                    if airplane.fuel == 0:
                        print(f'Airplane {airplane.id} has run out of fuel and must land.')
                        Airport.airplanes.remove(airplane)
'''

