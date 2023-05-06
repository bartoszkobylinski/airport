import time
from plane_class import Airplane

airplane = Airplane()


def handle_landing_permission(airplane):
    landing_permission_message = airplane.request_landing_permission()
    airplane.send_json(landing_permission_message)
    message = airplane.recv_json()
    airplane.receive_approach_permission(message)
    print()


def fly_randomly_and_handle_collisions(airplane):
    message = airplane.airplane_flight.fly_randomly()
    airplane.send_json(message)
    airport_message = airplane.recv_json()
    if airport_message.get("message", '') == "collision!":
        return True
    elif airport_message is None:
        print("Airport closed the connection")
        airplane.socket.close()
        return True
    return False


def request_runway_permission_and_inbound(airplane):
    message = airplane.request_runway_permission()
    airplane.send_json(message)
    airport_message = airplane.recv_json()
    if airport_message.get("message", '') == "permission granted":
        airplane.grant_permission_for_inbounding(airport_message)
        corridor_coordinates = airplane.grant_permission_for_inbounding(airport_message)
        return corridor_coordinates
    return None


def fly_to_corridor_and_land(airplane, corridor_coordinates):
    runway_coordinates = airplane.extract_runway_coordinates(corridor_coordinates)
    airplane_coordinates = airplane.airplane_flight.fly_to_corridor(
        runway_coordinates[0], runway_coordinates[1], runway_coordinates[2])
    airplane.send_json(airplane_coordinates)
    return airplane.airplane_flight.landed


def main(airplane):
    keep_running = True
    while keep_running:
        if airplane:
            '''
            landing_permission_message = airplane.request_landing_permission()
            airplane.send_json(landing_permission_message)
            message = airplane.recv_json()
            airplane.receive_approach_permission(message)
            '''
            handle_landing_permission(airplane)
            if not airplane.permission_granted:
                airplane.socket.close()
                keep_running = False
                continue
            while airplane.permission_granted and not airplane.airplane_flight.landed:
                '''
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
                '''
                collision = fly_randomly_and_handle_collisions(airplane)
                if collision:
                    break

                corridor_coordinates = request_runway_permission_and_inbound(airplane)
                '''
                if server_message.get("message", '') == "permission granted":
                    airplane.grant_permission_for_inbounding(server_message)
                    corridor_coordinates = airplane.grant_permission_for_inbounding(server_message)
                '''
                while airplane.inbound:
                    landed = fly_to_corridor_and_land(airplane, corridor_coordinates)
                    if landed:
                        airplane.socket.close()
                        keep_running = False
                        break
                    '''
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
                    '''

