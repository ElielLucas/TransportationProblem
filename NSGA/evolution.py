from utils_GA import NSGA2Utils
from utils_GA import Individuo
from population import Population
from tqdm import tqdm
from random import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

taxa_mutacao = 0.5

def plot_frente_de_pareto(populacao, geracao):
    custo_frente = np.array([populacao.fronts[0][i].of[0] for i in range(len(populacao.fronts[0]))])
    emissao_frente = np.array([populacao.fronts[0][i].of[1] for i in range(len(populacao.fronts[0]))])
    custo = np.array([populacao.fronts[i][j].of[0] for i in range(1, len(populacao.fronts)) for j in range(len(populacao.fronts[i]))])
    emissao = np.array([populacao.fronts[i][j].of[1] for i in range(1, len(populacao.fronts)) for j in range(len(populacao.fronts[i]))])
    plt.scatter(emissao,custo,c=np.array(['blue' for i in range(len(custo))]),label='Outras soluções')
    plt.scatter(emissao_frente, custo_frente, c=np.array(['red' for i in range(len(populacao.fronts[0]))]),label='Frente de pareto')
    plt.xlabel('Emissão de CO2')
    plt.ylabel('Custo do transporte')
    plt.title('ANSGA II - Geração '+ str(geracao))
    plt.legend()
    caminho = 'Figuras/' + ' - Geração('+str(geracao)+').png'
    plt.savefig(caminho)
    plt.close()
        
class Evolution:

    def __init__(self, num_of_generations=1000, num_of_individuals=75, tournament_prob=0.9, mutation_param=5):
        
        self.utils = NSGA2Utils(num_of_individuals, tournament_prob, mutation_param)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals

    def evolve(self):
        self.population = self.utils.create_initial_population()
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)
        
        children = self.utils.create_children(self.population)
        returned_population = None
        for i in tqdm(range(self.num_of_generations)):
            self.population.extend(children)
            
            children = self.utils.mutate(children)
                
            if i % 20 == 0:
                random_individuals = []
                while len(random_individuals) < self.num_of_individuals:
                    new_indiv = Individuo(montar_solução_random=True)
                    ok = True
                    for i in self.population.individuos:
                        if i.of == new_indiv.of: 
                            ok = False
                            break
                    if ok: random_individuals.append(new_indiv)   
    
                self.population.extend(random_individuals)
            
            # aux1 = []
            # aux2 = []
            # for i in self.population.individuos:
            #     aux1.append(i.of[0])
            #     aux2.append(i.of[1])
            
            # seila_df = pd.DataFrame({'of1': aux1,
            #                          'of2': aux2})
            # pd.set_option('display.float_format', '{:.8f}'.format)
            # breakpoint()
            # print(seila_df[seila_df['of1'].round(8).duplicated(keep=False)])
                
            self.utils.fast_nondominated_sort(self.population)
            new_population = Population()
            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1
            
            self.utils.calculate_crowding_distance(self.population.fronts[front_num])
            
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals - len(new_population)])
            
            returned_population = self.population
            self.population = new_population
            
            self.utils.fast_nondominated_sort(self.population)
            
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
                
            # breakpoint()
            plot_frente_de_pareto(self.population, i)
            children = self.utils.create_children(self.population)
            

        return returned_population
    
    
        

otm = Evolution()
result_omtz = otm.evolve()
for sol in result_omtz:
    print(sol.of)