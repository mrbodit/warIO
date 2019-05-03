from Anaconda2.Lib import os

from src.functions import *
from src.let_them_fight import let_them_fight


def generate_population(fitness,weights_length,biases_length,generations,number_of_objects):
    if generations == 0:
        number = int(input("Enter number of objects: "))
    else:
        number = number_of_objects
    population = []
    if len(fitness) == 0:
        for i in range(0, number):
            dir_name = "D:\\projekty\\warIO\\src\\population\\object" + str(i)
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            file_weights = open(dir_name + "\\weights.txt", "w+")
            file_biases = open(dir_name + "\\biases.txt", "w+")
            draw_weights(file_weights)
            draw_biases(file_biases)
            file_weights.close()
            file_biases.close()
            fitness.append(0)

    else:
        for i in range(number):
            if len(fitness) <= i:
                fitness.append(0)
            population.append(create_new_individual(fitness,weights_length,biases_length))

        for i in range(number):
            dir_path = "D:\\projekty\\warIO\\src\\population\\object" + str(i)
            file_weights = open(dir_path + "\\weights.txt", "w+")
            file_biases = open(dir_path + "\\biases.txt", "w+")
            for j in range(len(population[i][0])):
                file_biases.write(str(population[i][0][j]))
            for j in range(len(population[i][1])):
                file_weights.write(str(population[i][1][j]))
            file_weights.close()
            file_biases.close()
    if number != len(fitness):
        for i in range(number,len(fitness)):
            fitness.pop(-1)
