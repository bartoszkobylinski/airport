from .plane_class import Airplane, Status
import time

airplane = Airplane()


def main(plane):
    while plane.status not in {Status.WAITING, Status.LANDED, Status.CRASHED}:
        landing_permission_message = plane.request_landing_permission()
        pass
