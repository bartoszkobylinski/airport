import itertools
import math
from itertools import combinations


class CollisionDetector:
    def __init__(self, airport):
        self.airport = airport

    @staticmethod
    def check_collision(airplane1, airplane2, limit=10):
        x1, y1 = airplane1.get("x"), airplane1.get("y")
        x2, y2 = airplane2.get("x"), airplane2.get("y")
        if not (isinstance(x1, int) and isinstance(y1, int) and isinstance(x2, int) and isinstance(y2, int)):
            return False
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if distance <= limit:
            print(f"distance is:{distance}")
            return True
        else:
            return False

    def check_for_collision(self):
        airplanes_copy = self.airport.airplanes.copy()
        for airplane_one, airplane_two in itertools.combinations(airplanes_copy, 2):
            if self.check_collision(airplane_one, airplane_two, limit=10):
                airplane_one_id = airplane_one.get('airplane_ID')
                airplane_two_id = airplane_two.get('airplane_ID')
                self.airport.remove_airplane_by_id(airplane_one_id)
                self.airport.remove_airplane_by_id(airplane_two_id)
                return {"airport_message": "collision!"}
        return {"airport_message": "no collision"}
