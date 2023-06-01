from .plane_class import Airplane, Status
import time


def main(plane):
    print("im here")
    print(plane.status)
    landing_permission_message = plane.request_landing_permission()
    print(landing_permission_message)
    plane.send_json(landing_permission_message)
    print(plane.status)
    message = plane.recv_json()
    print(f"I,ve got message: {message}")
    plane.receive_approach_permission(message)
    while plane.status not in {Status.WAITING, Status.LANDED, Status.CRASHED}:
        time.sleep(1)
        print("im in")
        landing_permission_message = plane.request_landing_permission()
        print(landing_permission_message)
        pass

