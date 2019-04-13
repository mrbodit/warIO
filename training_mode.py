import pygame
import math
import time
from src.generate_population import generate_population
from src.hero import Hero
from src.global_variables import *
from src.display_functions import *

from src.fight_mode import *
from src.let_them_fight import let_them_fight
from src.let_them_fight_population import let_them_fight_population
from src.replay import *
from src.player_vs_AI import *

def training():

    running = True
    counter = 0
    fitness = []
    number_of_generations = 0
    while running:

        screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        screen.fill((255, 255, 255))
        pygame.display.set_caption('Training menu')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    fitness.append(let_them_fight(counter))
                    counter += 1
                if event.key == pygame.K_r:
                    number = int(input("Enter number of replay: "))
                    replay("D:\\projekty\\warIO\\src\\population\\object" + str(number) + "\\replay.txt")

                if event.key == pygame.K_g:
                    generations = int(input("Enter number of generations: "))
                    number_of_objects = int(input("Enter number of objects: "))

                    for j in range(0, generations):
                        matches = []
                        for i in range(0, number_of_objects):
                            matches.append([])
                        number_of_generations += 1
                        generate_population(fitness, WEIGHTS_LENGTH, BIASES_LENGTH, generations, number_of_objects)
                        for i in range(0, number_of_objects):
                            for k in range(NUMBER_OF_MATCHES - len(matches[i])):
                                selfcheck = False
                                while not selfcheck:
                                    enemy_number = random.randrange(0, number_of_objects)
                                    if enemy_number != i:
                                        selfcheck = True
                                [a, b] = let_them_fight_population(i, enemy_number)
                                matches[i].append(a)
                                matches[enemy_number].append(b)
                        for i in range(0, number_of_objects):
                            fitness[i] = sum(matches[i]) / len(matches[i])
                        print(fitness)
                        print("generacja: " + str(number_of_generations) + "  average fitness: " + str(sum(fitness) / len(fitness)))

                if event.key == pygame.K_y:
                    generations = int(input("Enter number of generations: "))
                    number_of_objects = int(input("Enter number of objects: "))
                    for j in range(0,generations):
                        number_of_generations += 1
                        generate_population(fitness,WEIGHTS_LENGTH,BIASES_LENGTH,generations,number_of_objects)
                        for i in range(0,number_of_objects,2):
                            [a,b] = let_them_fight_population(i,i+1)
                            fitness[i] = a
                            fitness[i+1] = b
                        print("generacja: " + str(number_of_generations) + "  average fitness: " + str(sum(fitness) / len(fitness)))

                if event.key == pygame.K_h:
                    generations = int(input("Enter number of generations: "))
                    number_of_objects = int(input("Enter number of objects: "))
                    for j in range(0, generations):
                        matches = []
                        number_of_generations += 1
                        generate_population(fitness, WEIGHTS_LENGTH, BIASES_LENGTH, generations, number_of_objects)
                        for i in range(0, number_of_objects):
                            matches.append([])
                            for k in range(3):
                                [a,b] = let_them_fight_population(i, AI_PATH)
                                matches[i].append(a)
                            fitness[i] = sum(matches[i]) / len(matches[i])
                        print("generacja: " + str(number_of_generations) + "  average fitness: " + str(sum(fitness) / len(fitness)))

                if event.key == pygame.K_p:
                    for i in range(len(fitness)):
                        print("generacja: " + str( number_of_generations) + "   " + str(i) + ": " + str(fitness[i]))
                    print("generacja: " + str( number_of_generations) + "  average fitness: " + str(sum(fitness)/len(fitness)))


        display_text(screen, GAME_WIDTH / 2, 100, 'WARIO', 255, 0, 0, 90)
        display_text(screen, GAME_WIDTH / 2, 200, 'Ai vs Ai  (press "w" to start)', 0, 0, 0, 50)
        display_text(screen, GAME_WIDTH / 2, 300, 'Replay (press "r" to start)', 0, 0, 0, 50)
        display_text(screen, GAME_WIDTH / 2, 400, 'fitness (press "p" to start)', 0, 0, 0, 50)
        display_text(screen, GAME_WIDTH / 2, 500, 'generate populationsv2 (press "g" to start)', 0, 0, 0, 50)
        display_text(screen, GAME_WIDTH / 2, 600, 'generate populations (press "y" to start)', 0, 0, 0, 50)
        display_text(screen, GAME_WIDTH / 2, 700, 'generate populations vs one AI (press "h" to start)', 0, 0, 0, 50)

        pygame.display.update()



