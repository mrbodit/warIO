import pygame
import math
from src.hero import Hero
from src.global_variables import *
from src.display_functions import *

from src.training_mode import *
from src.fight_mode import *
from src.replay import *
from src.player_vs_AI import *
wario_image = pygame.image.load('D:\\projekty\\warIO\\images\\wario.jpg')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Tutorial 1')
running = True

initialize_images()
while running:
  screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
  screen.fill((255, 255, 255))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_w:
        fight_mode()
      if event.key == pygame.K_s:
        player_vs_AI()
      if event.key == pygame.K_r:
        replay('D:\\projekty\\warIO\\ai\\replay.txt')
      if event.key == pygame.K_t:
        training()
    if event.type == pygame.KEYUP:
      continue

  clock.tick(60)
  screen.blit(wario_image,(400, 400))
  display_text(screen, GAME_WIDTH / 2, 100, 'WARIO', 255, 0, 0, 90)
  display_text(screen, GAME_WIDTH / 2, 200, '1 vs 1 mode  (press "w" to start)', 0, 0, 0, 50)
  display_text(screen, GAME_WIDTH / 2, 300, 'player vs AI (press "s" to start)', 0, 0, 0, 50)
  display_text(screen, GAME_WIDTH / 2, 400, 'Replay (press "r" to start)', 0, 0, 0, 50)
  display_text(screen, GAME_WIDTH / 2, 500, 'Training (press "t" to start)', 0, 0, 0, 50)
  pygame.display.update()



