class Population:
    def __init__(self):
        self.individuos = []
        self.fronts = []
        self.rank_medio = 0
        self.melhor_rank = 0

    def __len__(self):
        return len(self.individuos)

    def __iter__(self):
        return self.individuos.__iter__()
    
    def calculate_of_population(self):
        self.of_population = []
        for i in self.individuos:
            self.of_population.append(i.of)


    def extend(self, new_individuals):
        self.individuos.extend(new_individuals)

    def append(self, new_individual):
        self.individuos.append(new_individual)