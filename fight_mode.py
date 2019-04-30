import pygame
import math

from src.display_functions import *
from src.global_variables import *
from src.hero import *
from src.functions import *
def fight_mode():
  clock = pygame.time.Clock()

  screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
  pygame.display.set_caption('fight mode')

  hero1 = Hero(100, 100, (0, 0, 255))
  hero2 = Hero(500, 500, (0, 255, 0))
  heroes = [hero1,hero2]
  running = True
  d_pressed = False
  a_pressed = False
  left_pressed = False
  right_pressed = False

  while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          hero1.fire_bullet(hero1.bullets)
        if event.key == pygame.K_d:
          d_pressed = True
        if event.key == pygame.K_a:
          a_pressed = True

        if event.key == pygame.K_LEFT:
          left_pressed = True
        if event.key == pygame.K_RIGHT:
          right_pressed = True
        if event.key == pygame.K_UP:
          hero2.fire_bullet(hero2.bullets)

      if event.type == pygame.KEYUP:
        if event.key == pygame.K_d:
          d_pressed = False
        if event.key == pygame.K_a:
          a_pressed = False
        if event.key == pygame.K_LEFT:
          left_pressed = False
        if event.key == pygame.K_RIGHT:
          right_pressed = False



    if d_pressed:
      hero1.rotate("right")
    if a_pressed:
      hero1.rotate("left")

    if right_pressed:
      hero2.rotate("right")
    if left_pressed:
      hero2.rotate("left")

    execute_collision(heroes,hero1,hero2)

    clock.tick(60)

    hero1.movement(hero1.speed,hero2)
    display_hero(hero1,screen)
    for bullet in hero1.bullets:
      display_bullet(bullet, screen)

    hero2.movement(hero2.speed, hero1)
    display_hero(hero2, screen)
    for bullet in hero2.bullets:
      display_bullet(bullet, screen)


    display_text(screen,60,20,'health: ' + str(hero1.health),255,0,0,20)
    display_text(screen, 700, 20, 'health: ' + str(hero2.health), 255, 0, 0, 20)
    pygame.display.update()



