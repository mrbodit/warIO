import random

import pygame
import math

from src.display_functions import *
from src.global_variables import *
from src.hero import *
from src.dff_neural_network import *
from src.functions import *
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
    #ai.draw_weights(file_weights)
    #ai.draw_biases(file_biases)
    #file_weights.close()
    #file_biases.close()

    ai.get_weights("D:\\projekty\\warIO\\ai\\weights.txt")
    ai.get_biases("D:\\projekty\\warIO\\ai\\biases.txt")
    write_start_to_replay(replay, hero1, hero2)

    while running:

        screen.fill((255, 255, 255))
        replay_string = ["_","_","_","_","_","_"]

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
                if event.key == pygame.K_EQUALS:
                    fps = fps * 2
                if event.key == pygame.K_MINUS:
                    fps = round(fps / 2)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    d_pressed = False
                if event.key == pygame.K_a:
                    a_pressed = False

        inputs = return_inputs(hero2,hero1)
        ai_move = ai.calculate_output(inputs)


        do_ai_moves(ai_move[-1],replay_string,hero2)

        if d_pressed:
            hero1.rotate("right")
            replay_string[1] = "d"
        if a_pressed:
            hero1.rotate("left")
            replay_string[2] = "a"



        execute_collision(heroes,hero1,hero2)

        replay.write(''.join(replay_string) + "\n")
        clock.tick(fps)

        for hero in heroes:
            hero.movement()
            display_hero(hero, screen)
            for bullet in hero.bullets:
                display_bullet(bullet, screen)


        print(replay_string)

        display_network(screen,840,50,ai,ai_move)
        pygame.draw.rect(screen,[0,0,0],[GAME_WIDTH,0,5,GAME_HEIGHT])
        display_magazine(screen,60,60,hero1.magazine,hero1.reload)
        display_magazine(screen,700,60,hero2.magazine,hero2.reload)
        display_text(screen, 60, 20, 'health: ' + str(hero1.health), 255, 0, 0, 20)
        display_text(screen, 700, 20, 'health: ' + str(hero2.health), 255, 0, 0, 20)
        display_text(screen, GAME_WIDTH / 2, 20, 'FPS: ' + str(fps), 255, 0, 0, 20)
        pygame.display.update()




def do_ai_moves(output,replay_string,hero2):
    if output[0] > 0.5:
        hero2.rotate("left")
        replay_string[5] = "a"

    if output[1] > 0.5:
        hero2.rotate("right")
        replay_string[4] = "d"

    if output[2] > 0.5:
        hero2.fire_bullet(hero2.bullets)
        replay_string[3] = "w"