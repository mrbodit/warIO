import pygame
import math

from src.display_functions import *
from src.functions import execute_collision, score
from src.global_variables import *
from src.hero import *
from src.treasure import Treasure, treasure_collision


def replay(replay_path):
  clock = pygame.time.Clock()
  fps = 60

  screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
  pygame.display.set_caption('REPLAY')
  replay = [line.rstrip('\n') for line in open(replay_path)]

  hero1 = Hero(int(replay[0]), int(replay[1]), (0, 0, 255))
  hero2 = Hero(int(replay[3]), int(replay[4]), (0, 255, 0))
  hero1.angle = float(replay[2])
  hero2.angle = float(replay[5])
  heroes = [hero1,hero2]
  treasure = None
  running = True


  string_counter = STRINGS_AT_START
  replay_length = len(replay)
  while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_EQUALS:
          fps = fps * 2
        if event.key == pygame.K_MINUS:
          fps = round(fps / 2)

    if len(replay[string_counter]) < 6:
      x = int(replay[string_counter])
      y = int(replay[string_counter + 1])
      treasure = Treasure(x, y)
      string_counter += 2

    if replay[string_counter][0] == "w":
        hero1.fire_bullet(hero1.bullets)

    if replay[string_counter][1] == "d":
        hero1.rotate("right")

    if replay[string_counter][2] == "a":
        hero1.rotate("left")

    if replay[string_counter][3] == "s":
        hero1.teleport()

    if replay[string_counter][6] == "a":
        hero2.rotate("left")

    if replay[string_counter][5] == "d":
        hero2.rotate("right")

    if replay[string_counter][4] == "w":
        hero2.fire_bullet(hero2.bullets)

    if replay[string_counter][7] == "s":
        hero2.teleport()

    execute_collision(heroes,hero1,hero2)
    treasure = treasure_collision([hero1, hero2], treasure)
    clock.tick(fps)

    hero1.movement(hero1.speed,hero2)
    display_hero(hero1,screen)
    for bullet in hero1.bullets:
      display_bullet(bullet, screen)

    hero2.movement(hero2.speed, hero1)
    display_hero(hero2, screen)
    for bullet in hero2.bullets:
      display_bullet(bullet, screen)

    display_everything_except_animations(screen, hero1, hero2, treasure, score)
    pygame.display.update()
    string_counter += 1
    if string_counter >= replay_length:
      running = False


