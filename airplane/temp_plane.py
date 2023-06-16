from .plane_class import Airplane, Status
import time


def main(plane):
    if plane.status is Status.WAITING:
        landing_permission_message = plane.request_landing_permission()
        plane.send_json(landing_permission_message)
        message = plane.recv_json()
        plane.receive_approach_permission(message)
    while plane.status not in {Status.WAITING, Status.LANDED, Status.CRASHED}:
        plane.airplane_flight.fly()
        if plane.status is Status.APPROACHING:
            landing_permission_message = plane.request_runway_permission()
            plane.send_json(landing_permission_message)
            plane.recv_json()
            time.sleep(1)
    else:
        print("Airplane has either landed, crashed, or failed to receive permission to approach. Please refer to the "
              "log files for additional details.")
        print(plane.status)
        plane.socket.close()

