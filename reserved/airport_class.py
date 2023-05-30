import json
import threading
import math
import time
import logging

from socket_connection import SocketConnection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../airport.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



class Airport(SocketConnection):
    CORRIDOR_1_COORDS = (1000, 2000, 0)
    CORRIDOR_2_COORDS = (4000, 2000, 0)
    airplanes = []
    lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.x = 0
        self.y = 0
        self.z = 0
        self.airplanes = []
        self.runways = {1: False, 2: False}

    def handle_new_client(self, client_socket):
        while True:
            data = self.recv_json(client_socket)
            if data:
                action = data.get('data', '')
                time.sleep(1)
                response = self.process_action(action, data)
                self.send_json(response, custom_socket=client_socket)
            else:
                client_socket.close()
                break

    def process_action(self, action, data):
        action_to_function = {
            "request_landing_permission": (self.process_landing_permission_request, True),
            "execute_approach": (self.handle_fly, True),
            "request_runway_permission": (self.handle_inbound_request, True),
            "execute_runway_approach": (self.handle_inbound, True),
            "confirm_landing": (self.handle_landed, True)
        }
        func, requires_data = action_to_function.get(action, (self.handle_unknown_action, True))
        if requires_data:
            return func(data)
        else:
            return func()

    def process_landing_permission_request(self, data):
        response = self.grant_approach_permission(data)
        return response

    def grant_approach_permission(self, data):
        with self.lock:
            if len(self.airplanes) < 100:
                airplane = data.get("airplane_ID")
                self.airplanes.append(airplane)
                return {"airport_message": "Permission to approach airport granted"}
            else:
                return False

    def handle_fly(self, data):
        message = self.fly(data)
        return message

    def fly(self, data):
        airplane_ID = data.get("airplane_ID", '')
        x = int(data.get("x", '')) if "x" in data else ''
        y = int(data.get("y", '')) if "y" in data else ''
        z = int(data.get("z", '')) if "z" in data else ''
        airplane = dict()
        airplane.update(airplane_ID=airplane_ID, x=x, y=y, z=z)
        collision = self.check_all_collision(self.airplanes, specific_airplane=airplane)
        return collision

    def handle_inbound_request(self, data):
        response = self.inbound_for_approach_runway()
        return response

    def inbound_for_approach_runway(self):
        with self.lock:
            for runway_number, is_occupied in self.runways.items():
                if not is_occupied:
                    self.runways[runway_number] = True
                    corridor_coords = self.get_corridor_coordinates(runway_number)
                    return {'message': "permission granted",
                            "coordinates": {"x": corridor_coords[0], "y": corridor_coords[1], "z": corridor_coords[2]}}
            return {"message": "permission denied", "data": self.runways}

    def get_corridor_coordinates(self, runway_number):
        if runway_number == 1:
            return self.CORRIDOR_1_COORDS
        elif runway_number == 2:
            return self.CORRIDOR_2_COORDS

    def handle_inbound(self, data):
        message = self.inbounding(data)
        return message

    def handle_landed(self, data):
        airplane_id = data.get("airplane_ID", '')
        self.remove_airplane_by_id(airplane_id)
        coordinates = data.get("x_coordinates")
        with self.lock:
            for runway_number, (corridor_x, _, _) in enumerate([self.CORRIDOR_1_COORDS, self.CORRIDOR_2_COORDS], start=1):
                if coordinates == corridor_x:
                    self.runways[runway_number] = False
        return {"message": "Airplane landed"}

    def remove_airplane_by_id(self, airplane_id):
        with self.lock:
            self.airplanes = [airplane_id for airplane_id in self.airplanes if airplane_id != airplane_id]

    def handle_unknown_action(self, data):
        response = {"message": "Response: message received"}
        return response

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

    def check_all_collision(self, airplanes, limit=10, specific_airplane=None):
        if specific_airplane is None:
            specific_airplane_check = False
        else:
            specific_airplane_check = True

        for i in range(len(airplanes)):
            for j in range(i + 1, len(airplanes)):
                if specific_airplane_check:
                    if airplanes[i] != specific_airplane and airplanes[j] != specific_airplane:
                        continue

                if self.check_collision(airplanes[i], airplanes[j], limit=limit):
                    print("Airplanes collide")
                    message = {"message": "collision!", "airplane-1": airplanes[i], "airplane-2": airplanes[j]}
                    return message
        return {"message": "No collision detected"}

    def inbounding(self, data):
        airplane_ID = data.get("airplane_ID", '')
        x = data.get("x", '')
        y = data.get("y", '')
        z = data.get("z", '')
        airplane = dict()
        airplane.update(airplane_ID=airplane_ID, x=x, y=y, z=z)
        collision_status = self.check_all_collision(self.airplanes, specific_airplane=airplane)
        if collision_status["message"] == "No collision detected":
            response = {"message": "ok for inbounding"}
        else:
            response = collision_status
        return response

    def add_or_update_airplane_to_list(self, airplane_data):
        with self.lock:
            airplane_ID = airplane_data.get("airplane_ID", "")
            if airplane_ID not in [plane.get("airplane_ID") for plane in self.airplanes]:
                self.airplanes.append(airplane_data)
            else:
                for plane in self.airplanes:
                    if airplane_ID == plane.get("airplane_ID"):
                        plane.update(airplane_data)
                        break
