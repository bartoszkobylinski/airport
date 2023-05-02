import time
from plane_class import Airplane

airplane = Airplane()


def main(airplane):
    while True:
        if airplane:
            landing_permission_message = airplane.request_landing_permission()
            print(f"this is permission_for_landing: {landing_permission_message}")
            airplane.send_json(landing_permission_message)
            message = airplane.recv_json()
            print(f"this is airplane.permission_granted {airplane.permission_granted}")
            print(f"this is after receive permission  {message}")

            airplane.receive_approach_permission(message)
            print(f"this in airplane.permission_granted updated {airplane.permission_granted}")
            while airplane.permission_granted and not airplane.airplane_flight.landed:

                message = airplane.airplane_flight.fly_randomly()
                airplane.send_json(message)
                print(f"I have flu randomly: {message}")
                server_message = airplane.recv_json()
                if server_message.get("message") == "collision!":
                    break
                    pass  # create collision handling
                elif server_message is None:
                    print("Server closed the connection")
                    airplane.socket.close()
                    break
                print(f"Server has sent me this: {server_message}")
                time.sleep(1)

                message = airplane.request_runway_permission()
                print(f"I have sent permission to inbound to runway : {message}")
                airplane.send_json(message)
                server_message = airplane.recv_json()
                print(f"I got grant/reject for runway: {server_message}")
                if server_message.get("message", '') == "permission granted":
                    airplane.grant_permission_for_inbounding(server_message)
                    corridor_coordinates = airplane.grant_permission_for_inbounding(server_message)
                    print(f"!!!!!!!!!!!!!!!: {corridor_coordinates}")

                while airplane.inbound:
                    runway_coordinates = airplane.extract_runway_coordinates(corridor_coordinates)
                    print(f"this is coordinates of corridor: {runway_coordinates}")
                    airplane_coordinates = airplane.airplane_flight.fly_to_corridor(
                        runway_coordinates[0], runway_coordinates[1], runway_coordinates[2])
                    airplane.send_json(airplane_coordinates)

                    print(f"airplane landed: {airplane.airplane_flight.landed}")
                    if airplane.airplane_flight.landed:
                        print(f"waiting two seconds {time.sleep(2)}")
                        time.sleep(2)
                        airplane.socket.close()
                        break
                    else:
                        airplane_coordinates = airplane.airplane_flight.fly_to_corridor(
                            runway_coordinates[0], runway_coordinates[1], runway_coordinates[2])
                        airplane.send_json(airplane_coordinates)
