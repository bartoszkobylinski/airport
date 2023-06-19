import time


class PermissionHandler:
    def __init__(self, airport):
        self.airport = airport

    def process_landing_permission_request(self, data):
        response = self.inbound_for_approach_runway()
        return response

    def grant_approach_airport_permission(self, data):
        with self.airport.lock:
            if len(self.airport.airplanes) < 100:
                airplane = data.get("airplane_ID")
                self.airport.airplanes.append(airplane)
                return {"airport_message": "Permission to approach airport granted"}
            else:
                return {"airport_message": "Permission to approach airport rejected"}

    def handle_inbound_request(self, data):
        response = self.inbound_for_approach_runway()
        return response

    def inbound_for_approach_runway(self):
        with self.airport.lock:
            for runway in self.airport.runways:
                if not runway.is_occupied:
                    runway.is_occupied = True
                    corridor_coords = runway.corridor_coords
                    return {'airport_message': "permission granted",
                            "coordinates": {"x": corridor_coords[0], "y": corridor_coords[1], "z": corridor_coords[2]}}
            return {"airport_message": "permission denied"}

    def handle_inbound(self, data):
        message = self.airport.inbounding(data)
        return message
