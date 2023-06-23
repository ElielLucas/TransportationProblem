class Population:
    def __init__(self):
        self.individuos = []
        self.fronts = []

    def __len__(self):
        return len(self.individuos)

    def __iter__(self):
        return self.individuos.__iter__()

    def extend(self, new_individuals):
        self.individuos.extend(new_individuals)

    def append(self, new_individual):
        self.individuos.append(new_individual)