import math
import random
import numpy

from src.global_variables import *
from src.neuron import *


class DFF_Neural_Network:
    def __init__(self):
        self.input_layer = []
        self.hidden_layers = []
        self.output_layer = []
        self.all_layers = []
        self.weights = []
        self.biases = []
        self.number_of_weights = 0
        self.number_of_biases = 0

    def create_network(self):
        number_of_layers = NUMBER_OF_LAYERS
        table_of_layers = LAYERS
        if number_of_layers < 2:
            print('za mało warstw neuronów chyba')
            return False
        number = 1

        for i in range(number_of_layers):
            self.all_layers.append([])
            if i != 0 and i != (number_of_layers - 1):
                self.hidden_layers.append([])
            for j in range(table_of_layers[i]):
                neuron = Neuron(number)
                number += 1
                self.all_layers[i].append(neuron)
                if i == 0:
                    self.input_layer.append(neuron)
                elif i != (number_of_layers - 1):
                    self.hidden_layers[i - 1].append(neuron)
                else:
                    self.output_layer.append(neuron)

    def set_connections(self):
        for neuron1 in self.input_layer:
            for neuron2 in self.hidden_layers[0]:
                neuron1.children.append(neuron2)
                neuron2.parents.append(neuron1)
        if len(self.hidden_layers) > 1:
            for layer in range(len(self.hidden_layers) - 1):
                for neuron1 in self.hidden_layers[layer]:
                    for neuron2 in self.hidden_layers[layer + 1]:
                        neuron1.children.append(neuron2)
                        neuron2.parents.append(neuron1)
        for neuron1 in self.hidden_layers[len(self.hidden_layers) - 1]:
            for neuron2 in self.output_layer:
                neuron1.children.append(neuron2)
                neuron2.parents.append(neuron1)

    def draw_weights(self, file):
        for i in range(len(self.all_layers) - 1):
            for j in range(len(self.all_layers[i])):
                for k in range(len(self.all_layers[i][j].children)):
                    # file.write(str(random.gauss(0, 1) * math.sqrt(1 / len(self.all_layers[i]))) + '\n')
                    file.write(str(random.uniform(WEIGHTS_DOWN_CAP, WEIGHTS_TOP_CAP)) + '\n')

    def draw_biases(self, file):
        for i in range(1, len(self.all_layers)):
            for j in range(len(self.all_layers[i])):
                # file.write(str(random.gauss(0, len(self.all_layers[i - 1]))) + '\n')
                file.write(str(random.uniform(BIASES_DOWN_CAP, BIASES_TOP_CAP)) + '\n')

    def calculate_output(self, inputs):
        outcome = []
        weight_iterator = 0
        bias_iterator = 0
        for i in range(len(self.all_layers)):
            outcome.append([])
        for i in range(len(inputs)):
            outcome[0].append(inputs[i])
        for i in range(1, len(self.all_layers)):
            for j in self.all_layers[i]:
                outcome[i].append(0)
                for k in range(len(j.parents)):
                    outcome[i][-1] += outcome[i - 1][k] * self.weights[weight_iterator]
                    weight_iterator += 1
                outcome[i][-1] += self.biases[bias_iterator]
                bias_iterator += 1
                outcome[i][-1] = self.activation_function(outcome[i][-1])
        return outcome

    def activation_function(self, number):
        # return 1 / (1 + math.exp(-number))
        if number <= 0:
            return 0.01 * number
        else:
            return number

    def get_weights(self, file_path):
        self.number_of_weights = 0
        file = open(file_path, "r")
        for line in file:
            self.weights.append(float(line))
            self.number_of_weights += 1

    def get_biases(self, file_path):
        self.number_of_biases = 0
        file = open(file_path, "r")
        for line in file:
            self.biases.append(float(line))
            self.number_of_biases += 1
