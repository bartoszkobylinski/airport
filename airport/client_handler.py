import threading
import time
from db_manager import DbManager

from airport.airport_enums import Action, AirportResponse


class ClientHandler:
    def __init__(self, socket, airport, db_manager):
        self.socket = socket
        self.airport = airport
        self.db_manager = db_manager

    def handle_new_client(self, client_socket):
        status_mapping = {
            AirportResponse.APPROACH_AIRPORT_GRANTED.value: "approaching",
            AirportResponse.APPROACH_AIRPORT_REJECTED.value: "rejected for approach",
            AirportResponse.PERMISSION_GRANTED.value: "inbounding to runway",
            AirportResponse.PERMISSION_DENIED.value: "approaching",
            AirportResponse.AIRPLANE_LANDED.value: "landed"
        }
        while True:
            data = self.airport.recv_json(client_socket)
            if data:
                action = data.get("data", "")
                print(data)
                time.sleep(2)
                with self.airport.lock:
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
