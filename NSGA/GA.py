import utils_GA as ug
from random import random, choice, randint, randrange, sample
import time
import numpy as np
import pandas as pd
import os


n_iter = 1000000
n_pop = 50
def algoritmo_genetico():
    best_value = np.inf
    
    populacao = ug.criar_população(n_pop)
    of, fit = ug.update_fit(populacao)
    populacao, of, fit = ug.update_population(populacao, of, fit, n_pop)

    tempo_inicio = time.time()
    # Iteration procedure
    for it in range(n_iter):
        os.system('clear')
        tempo_att = time.time() - tempo_inicio
        print(tempo_att/60)
        if tempo_att >= 600:
            break
        new_population = []
        for ind in range(int(n_pop)):
            # Selection procedure
            escolha = random()
            if escolha <= 0.2:
                parent1, parent2 = ug.roulette_wheel_selection(populacao=populacao, fit=fit)
            else:
                parent1, parent2 = ug.tournament_selection(fit, populacao)
            
            # Crossover procedure
            if random() <= 0.6:  
                indiv_aleatorio = ug.Individuo(montar_solução_random=True)
                if choice([0, 1]) == 0:
                    child1, child2 = ug.crossover(parent1=parent1, parent2=indiv_aleatorio)
                else:
                    child1, child2 = ug.crossover(parent1=parent2, parent2=indiv_aleatorio)
            else:
                child1, child2 = ug.crossover(parent1=parent1, parent2=parent2)
            
            # Add in new population
            new_population.append(child1)
            new_population.append(child2)

        new_of, new_fit = ug.update_fit(new_population)
        
        populacao = populacao + new_population
        of = of + new_of
        fit = fit + new_fit
        
        populacao, of, fit = ug.update_population(populacao, of, fit, n_pop)
        if best_value > max(of):
            best_value = max(of)
            
    return best_value

list_resul = []
for i in range(10):
    list_resul.append(algoritmo_genetico())
    df = pd.DataFrame({'Inst.Grande - 11': list_resul})
    df.to_csv('resultados_teste.csv')
    
breakpoint()