from airplane_class.main_plain import main
from airplane_class.plane_class import Airplane
import argparse
import threading
import random
import time

'''
threads = []

parser = argparse.ArgumentParser()
parser.add_argument('--planes', type=int, default=random.randint(4, 15), help='Number of planes to spawn')
args = parser.parse_args()
number_of_planes = args.planes

while True:
    for _ in range(number_of_planes):
        airplane_class = Airplane()
        t = threading.Thread(target=main, args=[airplane_class])
        t.start()
        threads.append(t)

        threads = [t for t in threads if t.is_alive()]

    sleep_time = random.randint(5, 15)
    time.sleep(sleep_time)
'''


class AirplaneSimulator:
    def __init__(self, number_of_planes=random.randint(1, 3)):
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
