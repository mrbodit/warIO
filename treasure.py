import pygame
import math
from src.global_variables import *
from src.functions import *


class Treasure:
    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y
        self.radius = TREASURE_RADIUS

    def collide(self, object):
        if distance(self.position_x, self.position_y, object[0], object[1]) < self.radius + object[2]:
            return True
        return False

def treasure_collision(heroes,treasure):
    for hero in heroes:
        if treasure is not None:
            if treasure.collide([hero.position_x, hero.position_y, hero.radius]):
                hero.points += TREASURE_POINTS
                return None
    return treasure


def try_respawn_treasure(treasure):
    probability = random.randrange(0, TREASURE_PROBABILITY)
    if probability == 0 and treasure is None:
        treasure_x = random.randrange(TREASURE_RADIUS, GAME_HEIGHT - TREASURE_RADIUS)
        treasure_y = random.randrange(TREASURE_RADIUS, GAME_WIDTH - TREASURE_RADIUS)
        return Treasure(treasure_x, treasure_y)
    else:
        return treasure
