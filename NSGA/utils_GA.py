from individuo import Individuo
from random import random, choice, randint, randrange, sample, sample
import numpy as np
from typing import List
import time

class NSGA2Utils:
    def __init__(self, num_of_individuals, inp):     
        self.num_of_individuals = num_of_individuals
        self.inp = inp
    
    def create_children(self, population):
        children = []
        of_children = []
        population.calculate_of_population()
        while len(children) < len(population):
            parent1 = self.tournament(population)
            parent2 = parent1
            while parent1 == parent2:
                parent2 = self.tournament(population)
            
            if random() <= 0.6:  
                indiv_aleatorio = Individuo(montar_solução_random=True)
                if choice([0, 1]) == 0:
                    child1, child2 = self.crossover(parent1=parent1, parent2=indiv_aleatorio)
                else:
                    child1, child2 = self.crossover(parent1=parent2, parent2=indiv_aleatorio)
            else:
                child1, child2 = self.crossover(parent1=parent1, parent2=parent2)
            child1.calculate_objectives()
            child2.calculate_objectives()
            if (child1.of not in population.of_population and child1.of not in of_children):
                children.append(child1)
                of_children.append(child1.of)
            if (child2.of not in population.of_population and child2.of not in of_children):
                children.append(child2)
                of_children.append(child2.of)

        return children
    

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
        p = float(random.randint(1,100))/100.0
        qtd = int(len(self.populacao)/2)
        prole = []
        
        while qtd>0:
            parent1 = self.torneio()
            parent2 = self.torneio(adv = parent1)
            if p <= self.__probabilidade_crossover(parent1,parent2):
                prole += self.populacao[parent1]+self.populacao[parent2]
            qtd-=1
        self.populacao.individuos += prole
        
        child1 = Individuo(montar_solução_random=False)
        child2 = Individuo(montar_solução_random=False)
        self.montar_rotas_faltantes_1(child1, parent1, parent2)
        self.montar_rotas_faltantes_1(child2, parent2, parent1)
        return child1, child2


    def mutate(self, population):
        return Individuo(montar_solução_random=True)

     
    def montar_rotas_faltantes_1(self, child: Individuo, parent1, parent2):
        N = set(self.inp.N)
        K = set(self.inp.K)
        M = set(self.inp.M)
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
            for porto in self.inp.M:
                if alocacao_destinos[porto - self.inp.range_port] > 0:
                    alocacao_a_ser_distribuida = alocacao_destinos[porto - self.inp.range_port]
                    while alocacao_a_ser_distribuida > 0:
                        ponto_mais_proximo = choice(pontos_disponiveis)
                        if ponto_mais_proximo in K:
                            alocacao_ponto = alocacao_transbordos[ponto_mais_proximo - self.inp.range_trans]
                        elif ponto_mais_proximo in N:
                            alocacao_ponto = alocacao_origens[ponto_mais_proximo]

                        if alocacao_destinos[porto - self.inp.range_port] <= alocacao_ponto:
                            new_allocation = alocacao_destinos[porto - self.inp.range_port]
                        else:
                            excess = alocacao_destinos[porto - self.inp.range_port] - alocacao_ponto
                            new_allocation = alocacao_destinos[porto - self.inp.range_port] - excess
                            
                        if ponto_mais_proximo in K:
                            alocacao_transbordos[ponto_mais_proximo - self.inp.range_trans] -= new_allocation
                        elif ponto_mais_proximo in N:
                            alocacao_origens[ponto_mais_proximo] -= new_allocation

                        alocacao_a_ser_distribuida -= new_allocation
                        alocacao_destinos[porto - self.inp.range_port] -= new_allocation

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
        for node_ini in (self.inp.N + self.inp.K):
            if node_ini in rotas:
                for node_fim in list(rotas[node_ini]):
                    if node_fim in self.inp.M:
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
