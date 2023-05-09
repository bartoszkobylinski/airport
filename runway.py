class Runway:
    def __init__(self, number, corridor_coords):
        self.number = number
        self.corridor_coords = corridor_coords
        self.is_occupied = False

    def to_dict(self):
        return {
            "number": self.number,
            "corridor_coords": {
                "x": self.corridor_coords[0],
                "y": self.corridor_coords[1],
                "z": self.corridor_coords[2]
            },
            "is_occupied": self.is_occupied
        }