import pygame
import math
from src.global_variables import *
from src.functions import *
class bullet:
    def __init__(self,x,y,a):
        self.position_x = x
        self.position_y = y
        self.x_speed = 0
        self.y_speed = 0
        self.speed = BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.angle = a
        self.movement()
        self.movement()
        self.movement()
        self.movement()
    def movement(self):
        self.x_speed = self.speed * math.cos(self.angle)
        self.y_speed = self.speed * math.sin(self.angle)
        self.position_x = self.position_x + self.x_speed
        self.position_y = self.position_y + self.y_speed
        if self.position_x > 800 or self.position_y > 800 or self.position_y < 0 or self.position_x < 0:
            return True
    def collide(self,object):
        if distance(self.position_x,self.position_y,object[0],object[1]) < self.radius + object[2]:
            return True
        return False

    def is_out_of_boundaries(self):
        if self.position_x > GAME_WIDTH or self.position_y > GAME_HEIGHT or self.position_y < 0 or self.position_x < 0:
            return True