import json
import threading
import math
import time

from socket_connection import SocketConnection


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

    def send_json(self, client_socket, data):
        json_data = json.dumps(data)
        client_socket.send(json_data.encode(self.encoder))

    def recv_json(self, client_socket):
        try:
            data = client_socket.recv(self.buffer)
            if not data:
                return None
            json_data = json.loads(data.decode(self.encoder))
            print(json_data)
            return json_data
        except ConnectionResetError as error:
            print(f"Client got some problem with connection and is not connected to the server now")

    def handle_new_client(self, client_socket):
        while True:
            data = self.recv_json(client_socket)
            print(f"I've got data: {data}")
            time.sleep(5)
            if data:
                action = data.get('data', '')
                print(f"this is action: {action}")
                response = self.process_action(action, data)
                self.send_json(client_socket, response)
            else:
                print("Data has None value")
                continue

    def process_action(self, action, data):
        if action == "ask":
            return self.handle_ask()
        elif action == "fly":
            return self.handle_fly(data)
        elif action == "inbound_request":
            return self.handle_inbound_request(data)
        elif action == "inbound":
            return self.handle_inbound(data)
        elif action == "landed":
            return self.handle_landed()
        else:
            return self.handle_unknown_action()

    def handle_ask(self):
        print("Airport got question about permission to land")
        message = self.give_permission_to_approach()
        print(f"Message to airplane permission is: {message}")
        return message

    def handle_fly(self, data):
        message = self.fly(data)
        return message

    def handle_inbound_request(self, data):
        response = self.inbounding(data)
        print(f"This is what I can tell about INBOUND: {response}")
        return response

    def handle_inbound(self, data):
        message = self.inbounding(data)
        print("I'm inbounding")
        return message

    def handle_landed(self):
        self.socket.close()
        print("Airplane landed")
        return {"message": "Airplane landed"}

    def handle_unknown_action(self):
        print("Airplane send message with no case statement")
        response = {"message": "Response: message received"}
        return response


    def give_permission_to_approach(self):
        if len(self.airplanes) < 100:
            return {"message": True}
        else:
            return {"message": False}

    def inbound_for_landing(self):
        with self.lock:
            if self.runway1 and self.runway2:
                return {"message": "permission denied"}
            else:
                if self.runway1:
                    self.runway2 = True
                    return {'message': "permission granted",
                            "data": {"x": self.corridor_2_x, "y": self.corridor_2_y, "z": self.corridor_2_z}}
                else:
                    self.runway1 = True
                    return {'message': "permission granted",
                            "data": {"x": self.corridor_1_x, "y": self.corridor_1_y, "z": self.corridor_1_z}}

    def add_or_update_airplane_to_list(self, airplane_data):
        with self.lock:
            airplane_ID = airplane_data.get("airplane_ID", '')
            found = False
            if len(self.airplanes) > 0:
                for plane in self.airplanes:
                    if airplane_ID == plane.get("airplane_ID"):
                        plane.update(airplane_data)
                        found = True
                        break
                if not found:
                    self.airplanes.append(airplane_data)
            else:
                self.airplanes.append(airplane_data)

    def check_collision(self, airplane1, airplane2, limit=10):
        x1, y1 = airplane1.get("x"), airplane1.get("y")
        x2, y2 = airplane2.get("x"), airplane2.get("y")
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if distance < limit:
            return True
        else:
            return False

    def check_all_collision(self, airplanes, limit=10):
        for i in range(len(airplanes)):
            for j in range(i + 1, len(airplanes)):
                if self.check_collision(airplanes[i], airplanes[j], limit=limit):
                    print("Airplanes collide")
                    return {"message": f"Airplanes {airplanes[i]} and {airplanes[j]} collide!"}
                else:
                    continue

    def fly(self, data):
        airplane_ID = data.get("airplane_ID", '')
        x = data.get("x", '')
        y = data.get("y", '')
        z = data.get("z", '')
        airplane = dict()
        airplane.update(airplane_ID=airplane_ID, x=x, y=y, z=z)
        self.add_or_update_airplane_to_list(airplane_data=airplane)
        self.check_all_collision(self.airplanes)
        response = {"message": "ok"}
        return response

    def inbounding(self, data):
        airplane_ID = data.get("airplane_ID", '')
        x = data.get("coordinates", '').get("x", '')
        y = data.get("coordinates", '').get("y", '')
        z = data.get("coordinates", '').get("z", '')
        airplane = dict()
        airplane.update(airplane_ID=airplane_ID, x=x, y=y, z=z)
        self.add_or_update_airplane_to_list(airplane_data=airplane)
        response = {"message": "ok for inbounding"}
        self.check_all_collision(self.airplanes)
        return response
