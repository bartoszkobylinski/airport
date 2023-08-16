from airplane_class.main_plain import main
from airplane_class.plane_class import Airplane
import threading
import random
import time


class AirplaneSimulator:
    def __init__(self, number_of_planes=random.randint(87, 154)):
        self.number_of_planes = number_of_planes
        self.threads = []

    def run_simulation(self):
        while True:
            for _ in range(self.number_of_planes):
                airplane = Airplane()
                t = threading.Thread(target=main, args=[airplane])
                t.start()
                self.threads.append(t)

                self.threads = [t for t in self.threads if t.is_alive()]

            sleep_time = random.randint(450, 1500)
            time.sleep(sleep_time)
