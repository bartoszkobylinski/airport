import time

from random import choice
from datetime import datetime
from airport_class.airport_enums import Action
from airport_class.utils import get_plane_images


class ClientHandler:
    def __init__(self, socket, airport, db_manager):
        self.socket = socket
        self.airport = airport
        self.db_manager = db_manager

    def handle_new_client(self, client_socket):
        while True:
            data = self.airport.recv_json(client_socket)
            if data:
                action = data.get("data", "")
                print(data)
                time.sleep(0.1)
                with self.airport.lock:
                    data["timestamp"] = datetime.now()
                    data["image_url"] = choice(get_plane_images())
                    self.db_manager.add_row(**data)
                response = self.process_action(action, data)
                self.airport.send_json(response, custom_socket=client_socket)
            else:
                client_socket.close()
                break

    def process_action(self, action, data):
        action_to_function = {
            Action.APPROACH_AIRPORT_PERMISSION:
                (self.airport.permission_handler.grant_approach_airport_permission, True),
            Action.EXECUTE_APPROACH: (self.airport.handle_move_airplane, True),
            Action.RUNWAY_PERMISSION: (self.airport.permission_handler.handle_inbound_request, True),
            Action.RUNWAY_APPROACH: (self.airport.handle_move_airplane, True),
            Action.CONFIRM_LANDING: (self.airport.handle_landed, True)
        }
        func, requires_data = action_to_function.get(Action(action), (self.handle_unknown_action, True))
        if requires_data:
            return func(data)
        else:
            return func()

    @staticmethod
    def handle_unknown_action(data):
        response = {"message": f"airport get such data: {data} which is unknown for server"}
        return response
