import pygame
import math
import random
from src.bullet import bullet
from src.global_variables import *


class Hero:
    def __init__(self, x, y, color):
        self.position_x = x
        self.position_y = y
        self.x_speed = 0
        self.y_speed = 0
        self.radius = HERO_RADIUS
        self.speed = HERO_SPEED
        self.angle = (random.randrange(0, 100) / 50) * math.pi
        self.teleport_cooldown = TELEPORT_COOLDOWN
        self.magazine = 0
        self.reload = 0
        self.health = 10
        self.points = 0
        self.color = color
        self.bullets = [None, None, None]

    def movement(self):
        self.x_speed = self.speed * math.cos(self.angle)
        self.y_speed = self.speed * math.sin(self.angle)
        self.position_x = self.position_x + self.x_speed
        self.position_y = self.position_y + self.y_speed
        if self.position_x + self.radius > GAME_WIDTH:
            self.position_x = GAME_WIDTH - self.radius
        if self.position_x - self.radius < 0:
            self.position_x = 0 + self.radius
        if self.position_y + self.radius > GAME_HEIGHT:
            self.position_y = GAME_HEIGHT - self.radius
        if self.position_y - self.radius < 0:
            self.position_y = 0 + self.radius

        self.reload_bullets()
        self.cooldowns()
    def rotate(self, direction):
        if direction == "right":
            self.angle = self.angle + (HERO_ROTATION_SPEED * math.pi)
        else:
            self.angle = self.angle - (HERO_ROTATION_SPEED * math.pi)

        if self.angle > 2 * math.pi:
            self.angle = self.angle - 2 * math.pi
        if self.angle < 0:
            self.angle = self.angle + 2 * math.pi

    def fire_bullet(self, bullets):
        if self.magazine > 0:

            if self.bullets[0] == None:
                bullets[0] = bullet(self.position_x, self.position_y, self.angle)
                self.magazine -= 1
                return
            if self.bullets[1] == None:
                bullets[1] = bullet(self.position_x, self.position_y, self.angle)
                self.magazine -= 1
                return
            if self.bullets[2] == None:
                bullets[2] = bullet(self.position_x, self.position_y, self.angle)
                self.magazine -= 1
                return

    def cooldowns(self):
        self.teleport_cooldown -= 1
        if self.teleport_cooldown < 0:
            self.teleport_cooldown = 0

    def teleport(self):
        if self.teleport_cooldown == 0:
            self.position_x = GAME_WIDTH/2 - (self.position_x - (GAME_WIDTH/2))
            self.position_y = GAME_HEIGHT / 2 - (self.position_y - (GAME_HEIGHT / 2))
            self.teleport_cooldown = TELEPORT_COOLDOWN

    def reload_bullets(self):
        if self.magazine < 3:
            self.reload += 1
            if self.reload >= 60:
                self.magazine += 1
                self.reload = 0
