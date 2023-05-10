import math
class CollisionDetector:
    def __init__(self, airport):
        self.airport = airport

    def check_collision(self, airplane1, airplane2, limit=10):
        x1, y1 = airplane1.get("x"), airplane1.get("y")
        x2, y2 = airplane2.get("x"), airplane2.get("y")
        if not (isinstance(x1, int) and isinstance(y1, int) and isinstance(x2, int) and isinstance(y2, int)):
            return False
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if distance <= limit:
            return True
        else:
            return False

    def check_all_collision(self, limit=10, specific_airplane=None):
        if specific_airplane is None:
            specific_airplane_check = False
        else:
            specific_airplane_check = True

        for i in range(len(self.airport.airplanes)):
            for j in range(i + 1, len(self.airport.airplanes)):
                if specific_airplane_check:
                    if self.airport.airplanes[i] != specific_airplane and self.airport.airplanes[j] != specific_airplane:
                        continue

                if self.check_collision(self.airport.airplanes[i], self.airport.airplanes[j], limit=limit):
                    print("Airplanes collide")
                    message = {"airport_message": "collision!",
                               "airplane-1": self.airport.airplanes[i],
                               "airplane-2": self.airport.airplanes[j]}
                    return message
        return {"airport_message": "No collision detected"}
