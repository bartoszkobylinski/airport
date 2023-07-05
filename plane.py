from airplane.main_plain import main
from airplane.plane_class import Airplane
import argparse
import threading
import random
import time

threads = []

parser = argparse.ArgumentParser()
parser.add_argument('--planes', type=int, default=random.randint(4, 15), help='Number of planes to spawn')
args = parser.parse_args()
number_of_planes = args.planes

while True:
    for _ in range(number_of_planes):
        airplane = Airplane()
        t = threading.Thread(target=main, args=[airplane])
        t.start()
        threads.append(t)

        threads = [t for t in threads if t.is_alive()]

    sleep_time = random.randint(5, 15)
    time.sleep(sleep_time)
