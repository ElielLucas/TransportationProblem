class Population:
    def __init__(self):
        self.individuos = []
        self.fronts = []
        self.rank_medio = 0.0
        self.melhor_rank = 100000
        self.custo_medio = 0.0
        self.emissao_media = 0.0

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

    def calcula_dados(self):
        self.valor_medio = 0.0
        self.peso_medio = 0.0
        self.rank_medio = 0.0
        for i in range(self.__len__()):
            self.valor_medio += float(self.individuos[i].of[0])
            self.peso_medio += float(self.individuos[i].of[1])
            self.rank_medio += self.individuos[i].rank

        self.valor_medio /= float(self.__len__())
        self.peso_medio /= float(self.__len__())
        self.rank_medio /= float(self.__len__())
