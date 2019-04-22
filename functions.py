import math
import random
from src.display_functions import *

def int_from_string(string):
    number = input(string)
    try:
        intek = int(number)
    except:
        print("podałeś złego inta")
        return int_from_string(string)
    return intek
def distance(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return 1
    return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


def colliding_with_wall(x, y):
    if x >= GAME_WIDTH or x <= 0:
        return True
    if y >= GAME_HEIGHT or y <= 0:
        return True
    return False


def colliding_with_hero(x, y, hero):
    if distance(x, y, hero.position_x, hero.position_y) < hero.radius:
        return True
    return False


def colliding_with_bullet(x, y, bullet):
    if distance(x, y, bullet.position_x, bullet.position_y) < bullet.radius:
        return True
    return False


def draw_weights(file):
    for i in range(WEIGHTS_LENGTH):
        # file.write(str(random.gauss(0, 1) * math.sqrt(1 / len(self.all_layers[i]))) + '\n')
        file.write(str(random.uniform(WEIGHTS_DOWN_CAP, WEIGHTS_TOP_CAP)) + '\n')


def draw_biases(file):
    for i in range(BIASES_LENGTH):
        file.write(str(random.uniform(BIASES_DOWN_CAP, BIASES_TOP_CAP)) + '\n')


def angle(hero1, object):
    if hero1.position_y < object.position_y:
        angle = math.pi + math.acos((hero1.position_x - object.position_x) / (
            distance(hero1.position_x, hero1.position_y, object.position_x, object.position_y)))
        if angle + hero1.angle > math.pi * 2:
            return (angle + hero1.angle - math.pi * 2)
        else:
            return (angle + hero1.angle)
    else:
        angle = math.pi - math.acos((hero1.position_x - object.position_x) / (
            distance(hero1.position_x, hero1.position_y, object.position_x, object.position_y)))
        if angle + hero1.angle > math.pi * 2:
            return (angle + hero1.angle - math.pi * 2)
        else:
            return (angle + hero1.angle)


def distance_in_direction(x, y, angle, option, object):
    x_distance = x
    y_distance = y
    collide = False
    if option == "hero":
        while not collide:
            x_distance += math.cos(angle)
            y_distance += math.sin(angle)
            if colliding_with_hero(x_distance, y_distance, object) == True:
                return distance(x, y, x_distance, y_distance)
            if colliding_with_wall(x_distance, y_distance) == True:
                return 1200
    if option == "bullet":
        while not collide:
            x_distance += math.cos(angle)
            y_distance += math.sin(angle)
            for i in object:
                if i == None:
                    pass
                else:
                    if colliding_with_bullet(x_distance, y_distance, i) == True:
                        return distance(x, y, x_distance, y_distance)
            if colliding_with_wall(x_distance, y_distance) == True:
                return 1200
    else:
        while not collide:
            x_distance += math.cos(angle)
            y_distance += math.sin(angle)
            if colliding_with_wall(x_distance, y_distance) == True:
                return distance(x, y, x_distance, y_distance)


"""def distance_in_direction(x,y,angle,option,object):
    x_distance = x
    y_distance = y
    collide = False
    while not collide:
        x_distance += math.cos(angle)
        y_distance += math.sin(angle)
        if option == "hero":
            if colliding_with_hero(x_distance,y_distance,object) == True:
                return distance(x,y,x_distance,y_distance)
            if colliding_with_wall(x_distance,y_distance) == True:
                return 1200
        if option == "bullet":
            for i in object:
                if i == None:
                    pass
                else:
                    if colliding_with_bullet(x_distance,y_distance,i) == True:
                        return distance(x,y,x_distance,y_distance)
            if colliding_with_wall(x_distance,y_distance) == True:
                return 1200
        else:
            if colliding_with_wall(x_distance,y_distance) == True:
                return distance(x,y,x_distance,y_distance)"""


def execute_collision(heroes, hero1, hero2):
    for hero in heroes:
        counter = 0
        for bullet in hero.bullets:
            if bullet is not None:
                bullet.movement()
                if bullet.is_out_of_boundaries():
                    hero.bullets[counter] = None
                for h in heroes:
                    if bullet.collide([h.position_x, h.position_y, h.radius]):
                        if h == hero2:
                            hero2.health -= 1
                            hero1.bullets[counter] = None
                        else:
                            hero1.health -= 1
                            hero2.bullets[counter] = None
            counter += 1

def return_inputs(hero1, hero2, treasure):
    """   return [distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle, "hero", hero2) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle, "bullet", hero2.bullets) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle, "wall", None) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle + (0.25 * math.pi), "hero",
                                     hero2) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle + (0.25 * math.pi), "bullet",
                                     hero2.bullets) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle + (0.25 * math.pi), "wall",
                                     None) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle - (0.25 * math.pi), "hero",
                                     hero2) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle - (0.25 * math.pi), "bullet",
                                     hero2.bullets) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle - (0.25 * math.pi), "wall",
                                     None) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle + (0.5 * math.pi), "hero",
                                     hero2) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle + (0.5 * math.pi), "bullet",
                                     hero2.bullets) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle + (0.5 * math.pi), "wall",
                                     None) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle - (0.5 * math.pi), "hero",
                                     hero2) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle - (0.5 * math.pi), "bullet",
                                     hero2.bullets) / 1200,
               distance_in_direction(hero1.position_x, hero1.position_y, hero1.angle - (0.5 * math.pi), "wall",
                                     None) / 1200]"""
    bullets = []
    for i in range(len(hero2.bullets)):
        if hero2.bullets[i] == None:
            bullets.append([0, 0])
        else:
            bullets.append([1 - distance(hero1.position_x, hero1.position_y, hero2.bullets[i].position_x,
                                         hero2.bullets[i].position_y) / math.sqrt(GAME_WIDTH ** 2 + GAME_HEIGHT ** 2),
                            angle(hero1, hero2.bullets[i]) / (math.pi * 2)])
    if treasure is None:
        treasure_inputs = [0, 0]
    else:
        treasure_inputs = [(1 - distance(hero1.position_x,hero1.position_y, treasure.position_x,treasure.position_y) / math.sqrt(GAME_WIDTH ** 2 + GAME_HEIGHT ** 2)),
                                angle(hero1,treasure) / (math.pi * 2)]

    return ([abs((GAME_WIDTH / 2 - hero1.position_x) / (GAME_WIDTH / 2)),
             abs((GAME_HEIGHT / 2 - hero1.position_y) / (GAME_HEIGHT / 2)),
             1 - (distance(hero1.position_x, hero1.position_y, hero2.position_x, hero2.position_y) / math.sqrt(
                 GAME_WIDTH ** 2 + GAME_HEIGHT ** 2)),
             angle(hero1, hero2) / (math.pi * 2),
             bullets[0][0],
             bullets[0][1],
             bullets[1][0],
             bullets[1][1],
             bullets[2][0],
             bullets[2][1],
             treasure_inputs[0],
             treasure_inputs[1],
             hero1.magazine / 3,
             hero1.reload / 60,
             hero1.angle / (2 * math.pi),
             1 - (hero1.teleport_cooldown/TELEPORT_COOLDOWN),
             1 - (hero2.teleport_cooldown/TELEPORT_COOLDOWN),
             hero2.angle / (2 * math.pi)])
    # return([1 - (distance(hero1.position_x,hero1.position_y,hero2.position_x,hero2.position_y)/ math.sqrt(GAME_WIDTH ** 2 + GAME_HEIGHT ** 2)),
    #         angle(hero1,hero2)/ (math.pi * 2),])


def create_new_individual(fitness, weights_length, biases_length):
    best_fitness = max(fitness)
    average_fitness = int(sum(fitness) / len(fitness))
    weights = []
    biases = []
    dir_path = "D:\\projekty\\warIO\\src\\population\\object"
    passed = False

    for i in range(weights_length):
        while not passed:
            probability = random.randint(int(average_fitness), int(best_fitness))
            file_number = random.randrange(0, len(fitness))
            if fitness[file_number] >= probability:
                passed = True
        mutation = random.randint(1, 1001)
        if mutation <= MUTATION_RATE:
            weights.append(str(random.uniform(WEIGHTS_DOWN_CAP, WEIGHTS_TOP_CAP)) + '\n')
        else:
            file_path = dir_path + str(file_number) + "\\weights.txt"
            file = open(file_path)
            lines = file.readlines()
            weights.append(lines[i])
            file.close()

    for i in range(biases_length):
        while not passed:
            probability = random.randint(int(average_fitness), int(best_fitness))
            file_number = random.randrange(0, len(fitness))
            if fitness[file_number] >= probability:
                passed = True
        mutation = random.randint(1, 1001)
        if mutation <= MUTATION_RATE:
            biases.append(str(random.uniform(BIASES_DOWN_CAP, BIASES_TOP_CAP)) + '\n')
        else:

            file_path = dir_path + str(file_number) + "\\biases.txt"
            file = open(file_path)
            lines = file.readlines()
            biases.append(lines[i])
            file.close()
    return [biases, weights]
# def create_new_individual(fitness, weights_length, biases_length):
#     best_fitness = max(fitness)
#     average_fitness = int(sum(fitness) / len(fitness))
#     weights = []
#     biases = []
#     dir_path = "D:\\projekty\\warIO\\src\\population\\object"
#     passed = False
#
#     for i in range(weights_length):
#         while not passed:
#             probability = random.randint(int(average_fitness), int(best_fitness))
#             file_number = random.randrange(0, len(fitness))
#             if fitness[file_number] >= probability:
#                 passed = True
#         mutation = random.randint(1, 1001)
#         if mutation <= MUTATION_RATE:
#             weights.append(str(random.uniform(WEIGHTS_DOWN_CAP, WEIGHTS_TOP_CAP)) + '\n')
#         else:
#             file_path = dir_path + str(file_number) + "\\weights.txt"
#             file = open(file_path)
#             lines = file.readlines()
#             number = float(lines[i])
#             mini_mutation = random.randrange(1, 100)
#             if mini_mutation < 33:
#                 number += WEIGHTS_TOP_CAP / 400
#             if mini_mutation > 66:
#                 number -= WEIGHTS_TOP_CAP / 400
#             line = str(number) + '\n'
#             weights.append(line)
#             file.close()

    for i in range(biases_length):
        while not passed:
            probability = random.randint(int(average_fitness), int(best_fitness))
            file_number = random.randrange(0, len(fitness))
            if fitness[file_number] >= probability:
                passed = True
        mutation = random.randint(1, 1001)
        if mutation <= MUTATION_RATE:
            biases.append(str(random.uniform(BIASES_DOWN_CAP, BIASES_TOP_CAP)) + '\n')
        else:

            file_path = dir_path + str(file_number) + "\\biases.txt"
            file = open(file_path)
            lines = file.readlines()
            number = float(lines[i])
            mini_mutation = random.randrange(1, 100)
            if mini_mutation < 33:
                number += BIASES_TOP_CAP / 400
            if mini_mutation > 66:
                number -= BIASES_TOP_CAP / 400
            line = str(number) + '\n'
            biases.append(line)
            file.close()
    return [biases, weights]

def fitness_function(hero1, hero2):
    # return math.sqrt(GAME_HEIGHT **2 + GAME_WIDTH** 2) - distance(hero1.position_x,hero1.position_y,hero2.position_x,hero2.position_y)
    return score(hero1,hero2)

def score(hero1, hero2):
    return hero1.points + hero1.health * 10 + (100 - hero2.health * 10)

def write_start_to_replay(file, hero1, hero2):
    file.write(str(hero1.position_x) + '\n')
    file.write(str(hero1.position_y) + '\n')
    file.write(str(hero1.angle) + '\n')
    file.write(str(hero2.position_x) + '\n')
    file.write(str(hero2.position_y) + '\n')
    file.write(str(hero2.angle) + '\n')
