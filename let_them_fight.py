import math
import os

from src.dff_neural_network import DFF_Neural_Network
from src.functions import *
from src.global_variables import *
from src.hero import Hero


def let_them_fight(counter):
    dir_name_A = "D:\\projekty\\warIO\\src\\population\\object" + str(counter)
    dir_name_B = "D:\\projekty\\warIO\\src\\population\\object" + str(counter + 1)
    if not os.path.exists(dir_name_A):
        os.mkdir(dir_name_A)
    if not os.path.exists(dir_name_B):
        os.mkdir(dir_name_B)

    hero1_x = random.randrange(0,GAME_WIDTH)
    hero1_y = random.randrange(0,GAME_HEIGHT)
    hero1 = Hero(hero1_x, hero1_y, (0, 0, 255))
    hero2_x = random.randrange(0, GAME_WIDTH)
    hero2_y = random.randrange(0, GAME_HEIGHT)
    hero2 = Hero(hero2_x, hero2_y, (0, 255, 0))

    heroes = [hero1, hero2]
    running = True

    ai_A = DFF_Neural_Network()
    ai_A.create_network()
    ai_B = DFF_Neural_Network()
    ai_B.create_network()

    file_weights_A = open(dir_name_A + "\\weights.txt", "w+")
    file_biases_A = open(dir_name_A + "\\biases.txt", "w+")
    replay_A = open(dir_name_A + "\\replay.txt", "w+")
    file_weights_B = open(dir_name_B + "\\weights.txt", "w+")
    file_biases_B = open(dir_name_B + "\\biases.txt", "w+")
    replay_B = open(dir_name_B + "\\replay.txt", "w+")

    ai_A.draw_weights(file_weights_A)
    ai_A.draw_biases(file_biases_A)
    file_weights_A.close()
    file_biases_A.close()
    ai_B.draw_weights(file_weights_B)
    ai_B.draw_biases(file_biases_B)
    file_weights_B.close()
    file_biases_B.close()

    ai_A.get_weights(dir_name_A + "\\weights.txt")
    ai_A.get_biases(dir_name_A + "\\biases.txt")
    ai_B.get_weights(dir_name_B + "\\weights.txt")
    ai_B.get_biases(dir_name_B + "\\biases.txt")

    write_start_to_replay(replay_A,hero1,hero2)
    write_start_to_replay(replay_B, hero1, hero2)
    frames_counter = 0
    while running:
        replay_string = ["_", "_", "_", "_", "_", "_"]




        bullets_position = []
        for i in range(3):
            if hero2.bullets[i] == None:
                bullets_position.append([0, 0])
            else:
                bullets_position.append([hero2.bullets[i].position_x, hero2.bullets[i].position_y])

        inputs_a = return_inputs(hero1,hero2)
        ai_A_move = ai_A.calculate_output(inputs_a)


        inputs_b = return_inputs(hero2,hero1)
        ai_B_move = ai_B.calculate_output(inputs_b)

        do_ai_moves(ai_A_move[-1], replay_string, hero1,0)
        do_ai_moves(ai_B_move[-1], replay_string, hero2,1)

        execute_collision(heroes,hero1, hero2)

        replay_A.write(''.join(replay_string) + "\n")
        replay_B.write(''.join(replay_string) + "\n")


        for hero in heroes:
            hero.movement()
            if hero.health <= 0:
                running = False
            if frames_counter >= NUMBER_OF_FRAMES:
                running = False

        frames_counter += 1


    fitness_A = fitness_function(hero1,hero2)
    fitness_B = fitness_function(hero2,hero1)
    return [fitness_A,fitness_B]
def do_ai_moves(output, replay_string, hero, numer_of_hero):
    if output[0] > 0.5:
        hero.rotate("left")
        replay_string[numer_of_hero * 3 + 2] = "a"

    if output[1] > 0.5:
        hero.rotate("right")
        replay_string[numer_of_hero * 3 + 1] = "d"

    if output[2] > 0.5:
        hero.fire_bullet(hero.bullets)
        replay_string[numer_of_hero * 3 + 0] = "w"
