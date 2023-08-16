import logging
import time

from .plane_class import Status


def main(plane):
    if plane.status is Status.WAITING:
        approaching_permission_message = plane.request_landing_permission()
        plane.send_json(approaching_permission_message)
        message = plane.recv_json()
        plane.receive_approach_permission(message)
    while plane.status not in {Status.WAITING, Status.LANDED, Status.CRASHED}:
        flying_plane = plane.airplane_flight.fly()
        plane.send_json(flying_plane)
        airport_message = plane.recv_json()
        plane.airplane_flight.handle_collision(airport_message)
        if plane.status is Status.APPROACHING:
            landing_permission_message = plane.request_runway_permission()
            plane.send_json(landing_permission_message)
            airport_message = plane.recv_json()
            plane.receive_permission_to_descending(airport_message)

        while plane.status is Status.DESCENDING:
            message = plane.airplane_flight.fly(plane.airplane_flight.runway_coordinates[0],
                                                plane.airplane_flight.runway_coordinates[1],
                                                plane.airplane_flight.runway_coordinates[2])
            plane.send_json(message)
            airport_message = plane.recv_json()
            plane.airplane_flight.handle_collision(airport_message)

    else:
        logging.info(f"Airplane: {plane.airplane_flight.uniqueId} status: {plane.status} has either landed, crashed, or"
                     f"failed to receive permission to approach. Please refer to the log files for additional details.")
        plane.socket.close()
