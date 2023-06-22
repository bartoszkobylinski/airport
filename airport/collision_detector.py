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
            return True
        else:
            return False

    def check_for_collision(self):
        airplanes_copy = self.airport.airplanes.copy()
        for airplane_one, airplane_two in itertools.combinations(airplanes_copy, 2):
            if self.check_collision(airplane_one, airplane_two, limit=10):
                print("Airplanes collide")
                airplane_one_id = airplane_one.get('airplane_ID')
                airplane_two_id = airplane_two.get('airplane_ID')
                self.airport.remove_airplane_by_id(airplane_one_id)
                #print(f"I have removed {airplane_one_id} from the list")
                self.airport.remove_airplane_by_id(airplane_two_id)
                #print(f"I have removed {airplane_two_id} from the list")
                return {"airport_message": "collision!"}
        return {"airport_message": "no collision"}

    def check_all_collision(self, limit=10, specific_airplane=None):
        if specific_airplane is None:
            specific_airplane_check = False
        else:
            specific_airplane_check = True
        with self.airport.lock:
            for i in range(len(self.airport.airplanes)):
                for j in range(i + 1, len(self.airport.airplanes)):
                    if specific_airplane_check:
                        if self.airport.airplanes[i] != specific_airplane and \
                                self.airport.airplanes[j] != specific_airplane:
                            continue

                    if self.check_collision(self.airport.airplanes[i], self.airport.airplanes[j], limit=limit):
                        print("Airplanes collide")
                        message = {"airport_message": "collision!",
                                   "airplane-1": self.airport.airplanes[i],
                                   "airplane-2": self.airport.airplanes[j]}
                        self.airport.remove_airplane_by_id(self.airport.airplanes[i])
                        self.airport.remove_airplane_by_id(self.airport.airplanes[j])
                        return message
        return {"airport_message": "No collision detected"}
