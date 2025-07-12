import numpy as np

class Player:
    def __init__(self, id=None, x=0, y=0, angle=0, color=(255, 255, 255)):
        self.id = id
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.hit_damage = 10
        self.health = 100
        self.kills = 0
        self.damage_given = 0
        self.damage_queue = []
        self.radius = 0.1
        self.speed = 0.05
        self.rotation_speed = 0.05
    
    
    def rotate_left(self):
        self.angle -= self.rotation_speed
    
    
    def rotate_right(self):
        self.angle += self.rotation_speed
