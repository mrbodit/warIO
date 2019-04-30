import random

import pygame
import math

from src.display_functions import *
from src.global_variables import *
from src.hero import *
from src.dff_neural_network import *
from src.functions import *
from src.treasure import *


def player_vs_AI():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((GAME_WIDTH + 400, GAME_HEIGHT))
    pygame.display.set_caption('player vs AI')

    hero_x = random.randrange(0, GAME_WIDTH)
    hero_y = random.randrange(0, GAME_HEIGHT)
    hero1 = Hero(hero_x, hero_y, (0, 0, 255))
    hero_x = random.randrange(0, GAME_WIDTH)
    hero_y = random.randrange(0, GAME_HEIGHT)
    hero2 = Hero(hero_x, hero_y, (0, 255, 0))

    fps = 60
    heroes = [hero1, hero2]
    running = True
    d_pressed = False
    a_pressed = False

    ai = DFF_Neural_Network()
    ai.create_network()
    
    replay = open("D:\\projekty\\warIO\\ai\\replay.txt", "w+")

    ai.get_weights(AI_PATH + "\\weights.txt")
    ai.get_biases(AI_PATH + "\\biases.txt")

    treasure = None

    write_start_to_replay(replay, hero1, hero2)
    frames_counter = 0
    while running:

        screen.fill((255, 255, 255))
        replay_string = ["_", "_", "_", "_", "_", "_", "_", "_"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero1.fire_bullet(hero1.bullets)
                    replay_string[0] = "w"
                if event.key == pygame.K_d:
                    d_pressed = True
                if event.key == pygame.K_a:
                    a_pressed = True
                if event.key == pygame.K_s:
                    hero1.teleport()
                    replay_string[3] = "s"
                if event.key == pygame.K_EQUALS:
                    fps = fps * 2
                if event.key == pygame.K_MINUS:
                    fps = round(fps / 2)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    d_pressed = False
                if event.key == pygame.K_a:
                    a_pressed = False

        inputs = return_inputs(hero2, hero1,treasure)
        ai_move = ai.calculate_output(inputs)

        do_ai_moves(ai_move[-1], replay_string, hero2)

        if d_pressed:
            hero1.rotate("right")
            replay_string[1] = "d"
        if a_pressed:
            hero1.rotate("left")
            replay_string[2] = "a"


        if treasure is None:
            treasure_replay = False
        treasure = try_respawn_treasure(treasure)
        if treasure is not None and treasure_replay is False:
            replay.write(str(treasure.position_x) + "\n")
            replay.write(str(treasure.position_y) + "\n")
            treasure_replay is True

        execute_collision(heroes, hero1, hero2)
        treasure = treasure_collision([hero1, hero2], treasure)

        replay.write(''.join(replay_string) + "\n")
        clock.tick(fps)


        hero1.movement(hero1.speed, hero2)
        display_hero(hero1, screen)
        for bullet in hero1.bullets:
            display_bullet(bullet, screen)

        hero2.movement(hero2.speed, hero1)
        display_hero(hero2, screen)
        for bullet in hero2.bullets:
            display_bullet(bullet, screen)

        frames_counter += 1
        #display_network(screen,840,50,ai,ai_move)



        pygame.draw.rect(screen, [0, 0, 0], [GAME_WIDTH, 0, 5, GAME_HEIGHT])
        display_everything_except_animations(screen,hero1,hero2,treasure,score)
        pygame.display.update()


def do_ai_moves(output, replay_string, hero2):
    if output[0] > 0.5:
        hero2.rotate("left")
        replay_string[6] = "a"

    if output[1] > 0.5:
        hero2.rotate("right")
        replay_string[5] = "d"

    if output[2] > 0.5:
        hero2.fire_bullet(hero2.bullets)
        replay_string[4] = "w"

    if output[3] > 0.5:
        hero2.teleport()
        replay_string[7] = "s"