

class Player:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0.05
        self.rotation_speed = 0.05
    
    def rotate_left(self):
        self.angle -= self.rotation_speed
    
    def rotate_right(self):
        self.angle += self.rotation_speed