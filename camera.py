# camera.py



class Camera:
    def __init__(self):

        # Center of Camera
        self.x_coord: int = 0
        self.y_coord: int = 0
        self.zoom: float = 1

        self.speed = 25

    def move(self, dx, dy):
        self.x_coord += dx
        self.y_coord += dy

    def set_position(self, coordinate: [float, float]):
        self.x_coord = coordinate[0]
        self.y_coord = coordinate[1]
