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

    if replay[string_counter][5] == "a":
        hero2.rotate("left")

    if replay[string_counter][4] == "d":
        hero2.rotate("right")

    if replay[string_counter][3] == "w":
        hero2.fire_bullet(hero2.bullets)

    execute_collision(heroes,hero1,hero2)
    treasure = treasure_collision([hero1, hero2], treasure)
    clock.tick(fps)

    for hero in heroes:
      hero.movement()
      display_hero(hero,screen)
      for bullet in hero.bullets:
        display_bullet(bullet,screen)

    display_treasure(treasure, screen)
    display_text(screen,60,20,'health: ' + str(hero1.health),255,0,0,20)
    display_text(screen, GAME_WIDTH / 2, 20, 'Score1: ' + str(score(hero1,hero2)) + "   Score2: " + str(score(hero2, hero1)), 255, 0, 0, 18)
    display_magazine(screen, 60, 60, hero1.magazine, hero1.reload)
    display_magazine(screen, 700, 60, hero2.magazine, hero2.reload)
    display_text(screen, 700, 20, 'health: ' + str(hero2.health), 255, 0, 0, 20)
    pygame.display.update()
    string_counter += 1
    if string_counter >= replay_length:
      running = False


