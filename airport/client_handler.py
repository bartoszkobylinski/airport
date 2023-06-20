import threading
import time

from airport.airport_enums import Action, AirportResponse


class ClientHandler:
    def __init__(self, socket, airport):
        self.socket = socket
        self.airport = airport

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
            # print(f"this is data i got from client: {data}")
            time.sleep(2)
            if data:
                action = data.get("data", "")
                response = self.process_action(action, data)
                airport_message = response.get("airport_message", "")
                #print(f"airplanes: {self.airport.airplanes[0].get('airplane_ID','')}")
                self.airport.send_json(response, custom_socket=client_socket)
                print(f"airplanes: {self.airport.airplanes}")
            else:
                client_socket.close()
                break

    def process_action(self, action, data):
        action_to_function = {
            Action.APPROACH_AIRPORT_PERMISSION:
                (self.airport.permission_handler.grant_approach_airport_permission, True),
            #Action.EXECUTE_APPROACH: (self.airport.handle_fly, True),
            Action.EXECUTE_APPROACH: (self.airport.handle_move_airplane, True),
            Action.RUNWAY_PERMISSION: (self.airport.permission_handler.handle_inbound_request, True),
            #Action.RUNWAY_APPROACH: (self.airport.permission_handler.handle_inbound, True),
            Action.RUNWAY_APPROACH: (self.airport.handle_move_airplane, True),
            Action.CONFIRM_LANDING: (self.airport.handle_landed, True)
        }
        func, requires_data = action_to_function.get(Action(action), (self.handle_unknown_action, True))
        if requires_data:
            return func(data)
        else:
            return func()

    def handle_unknown_action(self, data):
        response = {"message": f"airport get such data: {data} which is unknown for server"}
        return response
