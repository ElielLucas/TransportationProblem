from individuo import Individuo, calcular_custo_e_emissao_transporte, find_nearest_neighbor, alocar_demanda
from random import random, choice, randint, randrange, sample, sample
from population import Population
import numpy as np
import defines as inp
from typing import List
import time

class NSGA2Utils:
    def __init__(self, num_of_individuals=50, tournament_prob=0.9, mutation_param=5):
        
        self.num_of_individuals = num_of_individuals
        self.tournament_prob = tournament_prob
        self.mutation_param = mutation_param
        
    def create_initial_population(self):
        population = Population()
        population.individuos = [Individuo(montar_solução_random=True) for _ in range(self.num_of_individuals)]
        return population
    
    
    def create_children(self, population):
        prob = float(randint(1,100))/100.0
        qtd = int(population.__len__())
        prole = []
        of_children = []
        population.calculate_of_population()
        while qtd > 0:
            parent1 = self.tournament(population=population)
            parent2 = self.tournament(adv = parent1, population=population)
            if prob <= self.probabilidade_crossover(parent1, parent2, population):                
                if random() <= 0.6:  
                    indiv_aleatorio = Individuo(montar_solução_random=True)
                    if choice([0, 1]) == 0:
                        child1, child2 = self.crossover(parent1=population.individuos[parent1], parent2=indiv_aleatorio)
                    else:
                        child1, child2 = self.crossover(parent1=population.individuos[parent2], parent2=indiv_aleatorio)
                else:
                    child1, child2 = self.crossover(parent1=population.individuos[parent1], parent2=population.individuos[parent2])

                child1.calculate_objectives()
                child2.calculate_objectives()
                
                if (child1.of not in population.of_population and child1.of not in of_children):
                    prole.append(child1)
                    of_children.append(child1.of)
                if (child2.of not in population.of_population and child2.of not in of_children):
                    prole.append(child2)
                    of_children.append(child2.of)
                qtd-=1

        return prole
    
    
    def tournament(self, adv=-1, population = None):
        lim = population.__len__()
        ret = randint(0,lim-1)
        for _ in range(0,3):
            other = randint(0,lim-1)
            while other == adv or other == ret:
                other = randint(0,lim-1)
            if population.individuos[other] < population.individuos[ret]:
                ret = other
        return ret
        
    
    def probabilidade_crossover(self, idx1, idx2, population):
        idx = idx1
        if(population.individuos[idx2].rank < population.individuos[idx1].rank):
            idx = idx2
        if(population.individuos[idx].rank > population.rank_medio) and population.melhor_rank < population.rank_medio:
            return (population.rank_medio - population.melhor_rank)/(population.rank_medio - population.melhor_rank)
        return 1.0
    
    # def tournament(self, population):
    #     # Seleciona dois indivíduos aleatórios
    #     ind1 = randint(0, len(population)-1)
    #     ind2 = randint(0, len(population)-1)
    #     if population.individuos[ind1].rank < population.individuos[ind2].rank:
    #         return population.individuos[ind1]
    #     elif population.individuos[ind1].rank > population.individuos[ind2].rank:
    #         return population.individuos[ind2]
    #     else:
    #         if population.individuos[ind1].crowding_distance > population.individuos[ind2].crowding_distance:
    #             return population.individuos[ind1]
    #         else:
    #             return population.individuos[ind2]


    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or ((individual.rank == other_individual.rank) and (
                        individual.crowding_distance > other_individual.crowding_distance)):
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
                front[0].crowding_distance = 10 ** 9
                front[solutions_num - 1].crowding_distance = 10 ** 9
                m_values = [individual.of[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0: scale = 1
                for i in range(1, solutions_num - 1):
                    front[i].crowding_distance += (front[i + 1].of[m] - front[i - 1].of[m]) / scale

    def crossover(self, parent1, parent2):
        child1 = Individuo(montar_solução_random=False)
        child2 = Individuo(montar_solução_random=False)
        self.montar_rotas_faltantes_1(child1, parent1, parent2)
        self.montar_rotas_faltantes_1(child2, parent2, parent1)
        return child1, child2

    
    def mutate(self, population):
        for e in range(population.__len__()):
            prob = float(randint(1, 100))/100.0
            if prob  <= self.probabilidade_mutacao(e, population):
                # breakpoint()
                new_indiv = Individuo(montar_solução_random=True)
                population.individuos[e] = new_indiv
        return population
    
    def probabilidade_mutacao(self, idx, population):
        if population.individuos[idx].rank <= population.rank_medio and population.melhor_rank < population.rank_medio:
            return 0.5*((float(population.individuos[idx].rank) - float(population.melhor_rank))/(float(population.rank_medio) - float(population.melhor_rank)))
        return 0.5

     
    def montar_rotas_faltantes_1(self, child: Individuo, parent1, parent2):
        N = set(inp.N)
        K = set(inp.K)
        M = set(inp.M)
        for i, cromo in enumerate(child.cromossomos):
            cromo.set_genes(
                gene_produtores=parent1.cromossomos[i].gene_produtores,
                gene_transbordos=parent1.cromossomos[i].gene_transbordos,
                gene_portos=parent2.cromossomos[i].gene_portos
            )

            rotas_parent1 = parent1.cromossomos[i].lista_adjacencia

            alocacao_destinos = cromo.gene_portos.copy()
            alocacao_transbordos = cromo.gene_transbordos.copy()
            alocacao_origens = cromo.gene_produtores.copy()
            
            for node_ini, aresta in rotas_parent1.items():
                for node_fim, custo in aresta.items():
                    if node_ini in N and node_fim in K:
                        alocacao_origens[node_ini] -= custo
                
            self.apagar_rotas_OD(rotas_parent1)
            pontos_disponiveis = list(N | K)
            for porto in inp.M:
                if alocacao_destinos[porto - inp.range_port] > 0:
                    alocacao_a_ser_distribuida = alocacao_destinos[porto - inp.range_port]
                    while alocacao_a_ser_distribuida > 0:
                        ponto_mais_proximo = choice(pontos_disponiveis)
                        if ponto_mais_proximo in K:
                            alocacao_ponto = alocacao_transbordos[ponto_mais_proximo - inp.range_trans]
                        elif ponto_mais_proximo in N:
                            alocacao_ponto = alocacao_origens[ponto_mais_proximo]

                        if alocacao_destinos[porto - inp.range_port] <= alocacao_ponto:
                            new_allocation = alocacao_destinos[porto - inp.range_port]
                        else:
                            excess = alocacao_destinos[porto - inp.range_port] - alocacao_ponto
                            new_allocation = alocacao_destinos[porto - inp.range_port] - excess
                            
                        if ponto_mais_proximo in K:
                            alocacao_transbordos[ponto_mais_proximo - inp.range_trans] -= new_allocation
                        elif ponto_mais_proximo in N:
                            alocacao_origens[ponto_mais_proximo] -= new_allocation

                        alocacao_a_ser_distribuida -= new_allocation
                        alocacao_destinos[porto - inp.range_port] -= new_allocation

                        if alocacao_ponto == 0:
                            pontos_disponiveis.remove(ponto_mais_proximo)

                        if new_allocation > 0:
                            rotas_parent1[ponto_mais_proximo][porto] = new_allocation
            cromo.lista_adjacencia = rotas_parent1

    
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


    def apagar_rotas_OD(self, rotas):
        for node_ini in (inp.N + inp.K):
            if node_ini in rotas:
                for node_fim in list(rotas[node_ini]):
                    if node_fim in inp.M:
                        del rotas[node_ini][node_fim]
                        
                        
                        
# Seleciona os pais para crossover usando torneio binário
# def selecao_torneio_binario(fronts):
#     pais_selecionados = []
#     while len(pais_selecionados) < 2:
#         indice_fronteira = random.randint(0, len(fronts) - 1)
#         fronteira = fronts[indice_fronteira]
#         indice_candidato1, indice_candidato2 = random.sample(range(len(fronteira)), 2)
#         pais_selecionados.append(fronteira[indice_candidato1] if funcao_fitness(fronteira[indice_candidato1]) <
#                                                             funcao_fitness(fronteira[indice_candidato2]) else
#                                fronteira[indice_candidato2])
#     return pais_selecionados
