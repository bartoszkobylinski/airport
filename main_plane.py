from plane_class import Airplane
import time

airplane = Airplane()


def handle_landing_permission(plane):
    landing_permission_message = plane.request_landing_permission()
    plane.send_json(landing_permission_message)
    message = plane.recv_json()
    plane.receive_approach_permission(message)


def fly_randomly_and_handle_collisions(plane):
    message = plane.airplane_flight.fly_randomly()
    plane.send_json(message)
    airport_message = plane.recv_json()
    if airport_message.get("airport_message", '') == "collision!":
        return True
    elif airport_message is None:
        print("Airport closed the connection")
        plane.socket.close()
        return True
    return False


def request_runway_permission_and_inbound(plane):
    message = plane.request_runway_permission()
    plane.send_json(message)
    airport_message = plane.recv_json()
    if airport_message.get("airport_message", '') == "permission granted":
        corridor_coordinates = plane.grant_permission_for_inbounding(airport_message)
        return corridor_coordinates
    return None


def fly_to_corridor_if_not_landed(plane, corridor_coordinates):
    runway_coordinates = plane.extract_runway_coordinates(corridor_coordinates)
    plane_coordinates = plane.airplane_flight.fly_to_corridor(
        runway_coordinates[0], runway_coordinates[1], runway_coordinates[2])
    plane.send_json(plane_coordinates)
    return plane.airplane_flight.landed


def main(plane):
    keep_running = True
    while keep_running:
        if plane:
            handle_landing_permission(plane)
            print(plane)
            if not plane.permission_granted:
                plane.socket.close()
                keep_running = False
                continue
            while plane.permission_granted and not plane.airplane_flight.landed:
                collision = fly_randomly_and_handle_collisions(plane)
                if collision:
                    break
                corridor_coordinates = request_runway_permission_and_inbound(plane)
                while plane.inbound:
                    landed = fly_to_corridor_if_not_landed(plane, corridor_coordinates)
                    if landed:
                        plane.socket.close()
                        keep_running = False
                        break
