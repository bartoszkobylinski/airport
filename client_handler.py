import time


class ClientHandler:
    def __init__(self, socket, airport):
        self.socket = socket
        self.airport = airport

    def handle_new_client(self, client_socket):
        while True:
            data = self.airport.recv_json(client_socket)
            if data:
                action = data.get("data", "")
                time.sleep(1)
                response = self.process_action(action, data)
                self.airport.send_json(response, custom_socket=client_socket)
            else:
                client_socket.close()
                break

    def process_action(self, action, data):
        action_to_function = {
            "request_landing_permission": (self.airport.permission_handler.process_landing_permission_request, True),
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
