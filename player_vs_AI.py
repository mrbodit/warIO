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
    ai.set_connections()

    ##file_biases = open("D:\\projekty\\warIO\\ai\\biases.txt", "w+")
    # file_weights = open("D:\\projekty\\warIO\\ai\\weights.txt", "w+")
    replay = open("D:\\projekty\\warIO\\ai\\replay.txt", "w+")
    # ai.draw_weights(file_weights)
    # ai.draw_biases(file_biases)
    # file_weights.close()
    # file_biases.close()

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



        for hero in heroes:
            hero.movement()
            display_hero(hero, screen)
            for bullet in hero.bullets:
                display_bullet(bullet, screen)

        frames_counter += 1
        # display_network(screen,840,50,ai,ai_move)

        pygame.draw.rect(screen, [0, 0, 0], [GAME_WIDTH, 0, 5, GAME_HEIGHT])
        display_treasure(treasure, screen)
        display_text(screen, GAME_WIDTH / 2, 60,'Score1: ' + str(score(hero1, hero2)) + "   Score2: " + str(score(hero2, hero1)), 255, 0, 0, 18)
        display_magazine(screen, 60, 60, hero1.magazine, hero1.reload)
        display_magazine(screen, 700, 60, hero2.magazine, hero2.reload)
        display_text(screen, 60, 80, 'teleport cd: ' + str(hero1.teleport_cooldown), 255, 0, 0, 20)
        display_text(screen, 700, 80, 'teleport cd: ' + str(hero2.teleport_cooldown), 255, 0, 0, 20)
        display_text(screen, 60, 20, 'health: ' + str(hero1.health), 255, 0, 0, 20)
        display_text(screen, 700, 20, 'health: ' + str(hero2.health), 255, 0, 0, 20)
        display_text(screen, GAME_WIDTH / 2, 20, 'FPS: ' + str(fps), 255, 0, 0, 20)
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