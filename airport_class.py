import json
import threading
import math
import time
import logging

from socket_connection import SocketConnection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Airport(SocketConnection):
    airplanes = []
    lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.runway1 = False
        self.runway2 = False
        self.x = 0
        self.y = 0
        self.z = 0
        self.corridor_1_x = 1000
        self.corridor_1_y = 2000
        self.corridor_1_z = 0
        self.corridor_2_x = 4000
        self.corridor_2_y = 2000
        self.corridor_2_z = 0

    def handle_new_client(self, client_socket):
        while True:
            data = self.recv_json(client_socket)
            logger.debug(f"Received data: {data}")
            if data:
                action = data.get('data', '')
                logger.debug(f"Action received: {action}")
                response = self.process_action(action, data)
                self.send_json(response, custom_socket=client_socket)  # Corrected call
            else:
                logger.warning("Received data has None value")
                client_socket.close()
                break

    def process_action(self, action, data):
        action_to_function = {
            "request_landing_permission": (self.process_landing_permission_request, False),
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

    def process_landing_permission_request(self):
        logger.info("Airport Control Tower: Received request for landing permission.")
        response = self.grant_approach_permission()
        logger.debug(f"Airport Control Tower: Response to airplane is: {response}")
        return response

    def grant_approach_permission(self):
        if len(self.airplanes) < 100:
            return {"airport_message": "Permission to approach airport granted"}
        else:
            return {"airport message": "Permission to approach airport denied."}

    def handle_fly(self, data):
        logger.debug(f"Handling fly action with TTTTTTT data: {data}")
        message = self.fly(data)
        logger.debug(f"Created response message: {message}")
        return message

    def fly(self, data):
        airplane_ID = data.get("airplane_ID", '')
        x = int(data.get("x", '')) if "x" in data else ''
        y = int(data.get("y", '')) if "y" in data else ''
        z = int(data.get("z", '')) if "z" in data else ''
        airplane = dict()
        airplane.update(airplane_ID=airplane_ID, x=x, y=y, z=z)
        self.add_or_update_airplane_to_list(airplane_data=airplane)
        collision = self.check_all_collision(self.airplanes, specific_airplane=airplane)
        return collision

    def handle_inbound_request(self, data):
        response = self.inbound_for_approach_runway()
        logger.debug(f"Inbound response: {response}")
        return response

    def inbound_for_approach_runway(self):
        with self.lock:
            if self.runway1 and self.runway2:
                return {"message": "permission denied", "data": {"1": self.runway1, "2": self.runway2}}
            else:
                if self.runway1:
                    self.runway2 = True
                    return {'message': "permission granted",
                            "coordinates": {"x": self.corridor_2_x, "y": self.corridor_2_y, "z": self.corridor_2_z}}
                else:
                    self.runway1 = True
                    return {'message': "permission granted",
                            "coordinates": {"x": self.corridor_1_x, "y": self.corridor_1_y, "z": self.corridor_1_z}}

    def handle_inbound(self, data):
        message = self.inbounding(data)
        logger.info("Handling inbound action")
        return message

    def handle_landed(self, data):
        airplane = data.get("airplane_ID", '')
        print(f"!!!!!!!!!!!: airplane {airplane}")
        if airplane in self.airplanes:
            print(f"self.airplanes: {self.airplanes}")
            self.airplanes.remove(airplane)
            print(f"airplane: {airplane} should be removed from airplanes: {self.airplanes}")
        coordinates = data.get("x_coordinates")
        print(f"this is coordinates of runway: {coordinates} and its type {type(coordinates)}")
        time.sleep(5)
        with self.lock:
            if coordinates == self.corridor_1_x:
                self.runway1 = False
            elif coordinates == self.corridor_2_x:
                self.runway2 = False
        logger.info("Airplane landed successfully")
        return {"message": "Airplane landed"}

    def handle_unknown_action(self, data):
        logger.warning("Airplane sent message with no case statement")
        response = {"message": "Response: message received"}
        return response

    def check_collision(self, airplane1, airplane2, limit=10):
        x1, y1 = airplane1.get("x"), airplane1.get("y")
        x2, y2 = airplane2.get("x"), airplane2.get("y")
        if not (isinstance(x1, int) and isinstance(y1, int) and isinstance(x2, int) and isinstance(y2, int)):
            return False
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        print(f"this is distance {distance}")
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
        self.add_or_update_airplane_to_list(airplane_data=airplane)
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
