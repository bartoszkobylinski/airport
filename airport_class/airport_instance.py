import threading

from .client_handler import ClientHandler
from .collision_detector import CollisionDetector
from .permission_handler import PermissionHandler
from airport_app.db_manager import DbManager
from .runway import Runway
from socket_connection import SocketConnection


class Airport(SocketConnection):
    def __init__(self):
        super().__init__()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.airplanes = []
        self.counter = 0
        self.runways = [Runway(1, (1000, 2000, 0)), Runway(2, (4000, 2000, 0))]
        self.lock = threading.Lock()
        self.collision_detector = CollisionDetector(self)
        self.permission_handler = PermissionHandler(self)
        self.db_manager = DbManager()
        self.client_handler = ClientHandler(self.socket, self, self.db_manager)

    def handle_new_client(self, client_socket):
        self.client_handler.handle_new_client(client_socket)

    def handle_landed(self, data):
        airplane_id = data.get("airplane_ID", '')
        self.remove_airplane_by_id(airplane_id)
        coordinates = data.get("x_coordinates")
        with self.lock:
            for runway in self.runways:
                if coordinates == runway.corridor_coords[0]:
                    runway.is_occupied = False
        return {"airport_message": "airplane_class landed"}

    def remove_airplane_by_id(self, airplane_id: str):
        with self.lock:
            for i, airplane in enumerate(self.airplanes):
                if airplane.get("airplane_id") == airplane_id:
                    del self.airplanes[i]
                    break

    def handle_move_airplane(self, data):
        message = self.move_airplane(data)
        return message

    def move_airplane(self, data):
        airplane_ID = data.get("airplane_ID", '')
        x = int(data.get("x", ''))
        y = int(data.get("y", ''))
        z = int(data.get("z", ''))
        status = str(data.get("status", ''))
        velocity = int(data.get("velocity", ''))
        fuel = int(data.get("fuel", ''))
        collision = self.collision_detector.check_for_collision()
        with self.lock:
            for airplane in self.airplanes:
                if airplane.get("airplane_ID") == airplane_ID:
                    airplane["x"] = x
                    airplane["y"] = y
                    airplane["z"] = z
                    airplane["status"] = status
                    airplane["velocity"] = velocity
                    airplane["fuel"] = fuel
                    break
        if status == "DESCENDING" and collision["airport_message"] == "No collision detected":
            response = {"airport_message": "ok for inbounding"}
        else:
            response = collision
        return response
