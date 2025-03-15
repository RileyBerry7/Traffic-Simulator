# camera.py



class Camera:
    def __init__(self):

        # Center of Camera
        self.x_coord: int = 0
        self.y_coord: int = 0
        self.zoom: float = 1

    def set_position(self, coordinate: [float, float]):
        self.x_coord = coordinate[0]
        self.y_coord = coordinate[1]
