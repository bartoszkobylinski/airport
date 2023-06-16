import threading
import time


class ClientHandler:
    def __init__(self, socket, airport):
        self.socket = socket
        self.airport = airport

    def handle_new_client(self, client_socket):
        status_mapping = {
            "Permission to approach airport granted": "approaching",
            "Permission to approach airport rejected": "rejected for approach",
            "permission granted": "inbounding to runway",
            "permission denied": "approaching",
            "airplane landed": "landed"
        }
        with self.airport.lock:
            self.airport.counter += 1
        while True:
            data = self.airport.recv_json(client_socket)
            print(f"this is data i got from client: {data}")
            time.sleep(2)
            if data:
                action = data.get("data", "")
                time.sleep(1)
                response = self.process_action(action, data)
                airport_message = response.get("airport_message", "")
                if airport_message in status_mapping:
                    airplane_data = {
                        'airplane_id': data.get("airplane_ID", ""),
                        'x': data.get("x", ""),
                        'y': data.get("y", ''),
                        'z': data.get("z", ''),
                        'fuel': data.get("fuel", ''),
                        'status': status_mapping[airport_message]
                    }
                self.airport.send_json(response, custom_socket=client_socket)
            else:
                client_socket.close()
                break

    def process_action(self, action, data):
        action_to_function = {
            "request_approaching_airport_permission":
                (self.airport.permission_handler.grant_approach_airport_permission, True),
            "execute_approach": (self.airport.handle_fly, True),
            "request_runway_permission": (self.airport.permission_handler.handle_inbound_request, True),
            "execute_runway_approach": (self.airport.permission_handler.handle_inbound, True),
            "confirm_landing": (self.airport.handle_landed, True)
        }
        func, requires_data = action_to_function.get(action, (self.handle_unknown_action, True))
        if requires_data:
            return func(data)
        else:
            return func()

    def handle_unknown_action(self, data):
        response = {"message": f"airport get such data: {data} which is unknown for server"}
        return response
