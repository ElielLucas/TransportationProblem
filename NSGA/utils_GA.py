from individuo import Individuo
from random import random, choice, randint
from population import Population

# from defines import Defines
import input as inp
import numpy as np

class NSGA2Utils:
    def __init__(self, num_of_individuals):
        self.num_of_individuals = num_of_individuals

    def create_initial_population(self):
        population = Population()
        population.individuos = [
            Individuo()
            for _ in range(self.num_of_individuals)
        ]
        return population

    def create_children(self, population):

        qtd = int(population.__len__())
        prole = []
        of_children = []
        population.calculate_of_population()
        # breakpoint()
        while qtd > 0:
            parent1 = self.tournament(population=population)
            parent2 = self.tournament(adv=parent1, population=population)
       
            child1, child2 = self.crossover(
                parent1=population.individuos[parent1],
                parent2=population.individuos[parent2],
            )

            child1.calculate_objectives()
            child2.calculate_objectives()

            prole.append(child1)
            of_children.append(child1.of)
            prole.append(child2)
            of_children.append(child2.of)

            qtd -= 2

        return prole

    def tournament(self, adv=-1, population=None):
        limite = population.__len__()
        retorno = randint(0, limite - 1)

        for _ in range(0, 3):
            other = randint(0, limite - 1)
            while other == adv or other == retorno:
                other = randint(0, limite - 1)
            if population.individuos[other] < population.individuos[retorno]:
                retorno = other
            elif population.individuos[retorno] == population.individuos[other]:
                if (
                    population.individuos[other].crowding_distance
                    < population.individuos[retorno].crowding_distance
                ):
                    retorno = other

        return retorno

    def probabilidade_crossover(self, idx, population):
        if population.individuos[idx].rank > population.rank_medio:
            return (population.rank_medio - population.melhor_rank) / (
                population.individuos[idx].rank - population.melhor_rank
            )

        if population.individuos[idx].rank <= population.rank_medio:
            return 1.0
        return 1.0

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or (
            (individual.rank == other_individual.rank)
            and (individual.crowding_distance > other_individual.crowding_distance)
        ):
            return 1
        else:
            return -1

    def choose_with_prob(self, prob):
        if random() <= prob:
            return True
        return False

    def fast_nondominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)

        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)

            i = i + 1
            population.fronts.append(temp)
        del population.fronts[i:]

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0
            for m in range(len(front[0].of)):
                front.sort(key=lambda individual: individual.of[m])
                front[0].crowding_distance = 10**9
                front[solutions_num - 1].crowding_distance = 10**9
                m_values = [individual.of[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0:
                    scale = 1
                for i in range(1, solutions_num - 1):
                    front[i].crowding_distance += (
                        front[i + 1].of[m] - front[i - 1].of[m]
                    ) / scale

    def crossover(self, parent1, parent2):
        crossover_point = randint(1, parent1.num_itens - 2)

        parent1.itens_escolhidos = parent1.itens_escolhidos[:crossover_point] + parent2.itens_escolhidos[crossover_point:]
        parent2.itens_escolhidos = parent2.itens_escolhidos[:crossover_point] + parent1.itens_escolhidos[crossover_point:]

        return (parent1, parent2)

    def mutate(self, population):
        for e in range(population.__len__()):
            if self.probabilidade_mutacao(e, population) >= 0.2:
                new_indiv = Individuo()
                if population.individuos[e].rank != 0:
                    population.individuos[e] = new_indiv
                else:
                    if new_indiv < population.individuos[e]:
                        population.individuos[e] = new_indiv

        return population

    def probabilidade_mutacao(self, idx, population):
        if (
            population.individuos[idx].rank <= population.rank_medio
            and population.melhor_rank < population.rank_medio
        ):
            return 0.5 * (
                (float(population.individuos[idx].rank) - float(population.melhor_rank))
                / (float(population.rank_medio) - float(population.melhor_rank))
            )

        return 0.5


    def get_fit(self, populacao):
        fit = [individuo.valor_fit for individuo in populacao]
        return fit

    def update_fit(self, populacao):
        OF = []
        FIT = []
        for individuo in populacao:
            of = individuo.objective_function()
            OF.append(of)
            FIT.append(individuo.calcular_fit(of=of))

        return OF, FIT

    def update_population(self, population, of, fit, n_pop):
        SORT_POSITIONS = np.argsort(of)
        new_population = []
        new_of = []
        new_fit = []

        for i in range(n_pop):
            new_population.append(population[SORT_POSITIONS[i]])
            new_of.append(of[SORT_POSITIONS[i]])
            new_fit.append(fit[SORT_POSITIONS[i]])

        return new_population, new_of, new_fit
