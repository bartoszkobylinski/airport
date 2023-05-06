import time
from plane_class import Airplane

airplane = Airplane()



def main(airplane):
    keep_running = True
    while keep_running:
        if airplane:
            landing_permission_message = airplane.request_landing_permission()
            print(f"this IS permission_for_landing: {landing_permission_message}")
            airplane.send_json(landing_permission_message)
            message = airplane.recv_json()
            airplane.receive_approach_permission(message)
            while airplane.permission_granted and not airplane.airplane_flight.landed:
                message = airplane.airplane_flight.fly_randomly()
                airplane.send_json(message)
                server_message = airplane.recv_json()
                if server_message.get("message") == "collision!":
                    break
                    pass  # create collision handling
                elif server_message is None:
                    print("Server closed the connection")
                    airplane.socket.close()
                    keep_running = False
                    break
                message = airplane.request_runway_permission()
                airplane.send_json(message)
                server_message = airplane.recv_json()
                if server_message.get("message", '') == "permission granted":
                    airplane.grant_permission_for_inbounding(server_message)
                    corridor_coordinates = airplane.grant_permission_for_inbounding(server_message)
                while airplane.inbound:
                    runway_coordinates = airplane.extract_runway_coordinates(corridor_coordinates)
                    airplane_coordinates = airplane.airplane_flight.fly_to_corridor(
                        runway_coordinates[0], runway_coordinates[1], runway_coordinates[2])
                    airplane.send_json(airplane_coordinates)
                    if airplane.airplane_flight.landed:
                        airplane.socket.close()
                        keep_running = False
                        break
                    else:
                        airplane_coordinates = airplane.airplane_flight.fly_to_corridor(
                            runway_coordinates[0], runway_coordinates[1], runway_coordinates[2])
                        airplane.send_json(airplane_coordinates)
