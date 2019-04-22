import math
import os

from src.dff_neural_network import DFF_Neural_Network
from src.functions import *
from src.global_variables import *
from src.hero import Hero
from src.treasure import try_respawn_treasure, treasure_collision


def let_them_fight_population(counter1,counter2):
    dir_name_A = "D:\\projekty\\warIO\\src\\population\\object" + str(counter1)
    if len(str(counter2)) <= 4:
        dir_name_B = "D:\\projekty\\warIO\\src\\population\\object" + str(counter2)
    else:
        dir_name_B = counter2
    if not os.path.exists(dir_name_A):
        os.mkdir(dir_name_A)
    if not os.path.exists(dir_name_B):
        os.mkdir(dir_name_B)

    hero1_x = random.randrange(0, GAME_WIDTH)
    hero1_y = random.randrange(0, GAME_HEIGHT)
    hero1 = Hero(hero1_x, hero1_y, (0, 0, 255))
    hero2_x = random.randrange(0, GAME_WIDTH)
    hero2_y = random.randrange(0, GAME_HEIGHT)
    hero2 = Hero(hero2_x, hero2_y, (0, 255, 0))

    heroes = [hero1, hero2]
    running = True

    ai_A = DFF_Neural_Network()
    ai_A.create_network()
    ai_A.set_connections()
    ai_B = DFF_Neural_Network()
    ai_B.create_network()
    ai_B.set_connections()

    treasure = None

    replay_A = open(dir_name_A + "\\replay.txt", "w+")
    replay_B = open(dir_name_B + "\\replay.txt", "w+")

    ai_A.get_weights(dir_name_A + "\\weights.txt")
    ai_A.get_biases(dir_name_A + "\\biases.txt")
    ai_B.get_weights(dir_name_B + "\\weights.txt")
    ai_B.get_biases(dir_name_B + "\\biases.txt")

    write_start_to_replay(replay_A, hero1, hero2)
    write_start_to_replay(replay_B, hero1, hero2)
    frames_counter = 0
    while running:
        replay_string = ["_", "_", "_", "_", "_", "_", "_", "_"]

        ai_A_move = ai_A.calculate_output(return_inputs(hero1, hero2, treasure))
        ai_B_move = ai_B.calculate_output(return_inputs(hero2, hero1, treasure))

        do_ai_moves(ai_A_move[-1], replay_string, hero1,0)
        do_ai_moves(ai_B_move[-1], replay_string, hero2,1)


        if treasure is None:
            treasure_replay = False
        treasure = try_respawn_treasure(treasure)
        if treasure is not None and treasure_replay is False:
            replay_A.write(str(treasure.position_x) + "\n")
            replay_A.write(str(treasure.position_y) + "\n")
            replay_B.write(str(treasure.position_x) + "\n")
            replay_B.write(str(treasure.position_y) + "\n")
            treasure_replay is True

        execute_collision(heroes, hero1, hero2)
        treasure = treasure_collision([hero1, hero2], treasure)

        replay_A.write(''.join(replay_string) + "\n")
        replay_B.write(''.join(replay_string) + "\n")


        for hero in heroes:
            hero.movement()
            if hero.health <= 0:
                running = False
            if frames_counter >= NUMBER_OF_FRAMES:
                running = False

        frames_counter += 1

    fitness_A = fitness_function(hero1, hero2)
    fitness_B = fitness_function(hero2, hero1)
    return [fitness_A,fitness_B]

def do_ai_moves(output, replay_string, hero, number_of_hero):
    if output[0] > 0.5:
        hero.rotate("left")
        replay_string[number_of_hero * 4 + 2] = "a"

    if output[1] > 0.5:
        hero.rotate("right")
        replay_string[number_of_hero * 4 + 1] = "d"

    if output[2] > 0.5:
        hero.fire_bullet(hero.bullets)
        replay_string[number_of_hero * 4 + 0] = "w"

    if output[3] > 0.5:
        hero.teleport()
        replay_string[number_of_hero * 4 + 3] = "s"