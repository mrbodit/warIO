class Neuron:
    def __init__(self,number):
        self.parents = []
        self.children = []
        self.number = number
    def add_neuron(self,neuron):
        self.children.append(neuron)