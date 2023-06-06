from individuo import Individuo, calcular_custo_transporte, find_nearest_neighbor, alocar_demanda
from random import random, choice, randint, randrange, sample
import numpy as np
import defines as inp
from typing import List


def criar_população(tamanho_populacao: int):
    return [Individuo(montar_solução_random=True) for _ in range(tamanho_populacao)]
        
        
def roulette_wheel_selection(populacao, fit):
    sum_fit = sum(fit)
    probabilidades = [aptidao / sum_fit for aptidao in fit]

    selecionados = np.random.choice(populacao, 2, replace = False, p = probabilidades)
    return (selecionados[0], selecionados[1])

def tournament_selection(fit, populacao):
    selecionados = []
    for i in range(len(populacao)):
      cromossomo_1 = randint(0, len(populacao)-1)
      cromossomo_2 = randint(0, len(populacao)-1)

      if fit[cromossomo_1] > fit[cromossomo_2]:
          selecionados.append(cromossomo_1)
      else:
          selecionados.append(cromossomo_2)
    return populacao[selecionados[0]], populacao[selecionados[1]]
       

def apagar_rotas_OD(rotas):
    for node in inp.K:
        if node in rotas:
            del rotas[node]
    
    apagar_arestas = []
    for node_ini in inp.N:
        if node_ini in rotas:
            for node_fim, custo in rotas[node_ini].items():
                if node_fim in inp.M:
                    apagar_arestas.append((node_ini, node_fim))
    
    for node_ini, node_fim in apagar_arestas:
        del rotas[node_ini][node_fim]


def apagar_rotas_OI_e_OD(rotas):
    for node in inp.N:
        if node in rotas:
            del rotas[node]
            

def apagar_rotas_OI_e_ID(rotas):
    apagar_arestas = []
    for node_ini in (inp.N + inp.K):
        if node_ini in rotas:
            for node_fim, custo in rotas[node_ini].items():
                if node_fim in (inp.K + inp.M):
                    apagar_arestas.append((node_ini, node_fim))
            
     
def montar_rotas_faltantes_1(child, parent1, parent2):
    
    for i, cromo in enumerate(child.cromossomos):
        cromo.set_genes(gene_produtores=parent1.cromossomos[i].gene_produtores,
                        gene_transbordos=parent1.cromossomos[i].gene_transbordos,
                        gene_portos=parent2.cromossomos[i].gene_portos)
        
        rotas_parent1 = parent1.cromossomos[i].lista_adjacencia
        
        alocacao_destinos = cromo.gene_portos.copy()
        alocacao_transbordos = cromo.gene_transbordos.copy()
        alocacao_origens = [0] * len(inp.N)
        
        # Passa os pesos das arestas para um vetor de origens que será distribuído novamente.
        for node_ini, aresta in rotas_parent1.items():
            for node_fim, custo in aresta.items():
                if node_ini in inp.N and node_fim in inp.M:
                    alocacao_origens[node_ini] += custo
                    
        apagar_rotas_OD(rotas_parent1)
        
        pontos_sem_capacidade = [] 
        for porto in inp.M:
            if alocacao_destinos[porto - inp.range_port] > 0:
                alocacao_a_ser_distribuida = alocacao_destinos[porto - inp.range_port]
                while alocacao_a_ser_distribuida > 0:
                    ponto_mais_proximo = find_nearest_neighbor(ponto_referencia=porto, possiveis_destinos=inp.N + inp.K, 
                                                               pontos_sem_capacidade=pontos_sem_capacidade)
                    if ponto_mais_proximo in inp.K:
                        if alocacao_destinos[porto - inp.range_port] <= alocacao_transbordos[ponto_mais_proximo - inp.range_trans]:
                            new_allocation = alocacao_destinos[porto - inp.range_port]
                            alocacao_transbordos[ponto_mais_proximo - inp.range_trans] -= new_allocation
                            alocacao_a_ser_distribuida -= new_allocation
                            alocacao_destinos[porto - inp.range_port] = 0
                        else:
                            excess = alocacao_destinos[porto - inp.range_port] - alocacao_transbordos[ponto_mais_proximo - inp.range_trans]
                            new_allocation = alocacao_destinos[porto - inp.range_port] - excess
                            alocacao_transbordos[ponto_mais_proximo - inp.range_trans] -= new_allocation
                            alocacao_destinos[porto - inp.range_port] -= new_allocation
                            alocacao_a_ser_distribuida -= new_allocation
                            
                        if alocacao_transbordos[ponto_mais_proximo - inp.range_trans] == 0:
                            pontos_sem_capacidade.append(ponto_mais_proximo)
                    elif ponto_mais_proximo in inp.N:
                        if alocacao_destinos[porto - inp.range_port] <= alocacao_origens[ponto_mais_proximo]:
                            new_allocation = alocacao_destinos[porto - inp.range_port]
                            alocacao_origens[ponto_mais_proximo] -= new_allocation
                            alocacao_a_ser_distribuida -= new_allocation
                            alocacao_destinos[porto - inp.range_port] = 0
                        else:
                            excess = alocacao_destinos[porto - inp.range_port] - alocacao_origens[ponto_mais_proximo]
                            new_allocation = alocacao_destinos[porto - inp.range_port] - excess
                            alocacao_origens[ponto_mais_proximo] -= new_allocation
                            alocacao_destinos[porto - inp.range_port] -= new_allocation
                            alocacao_a_ser_distribuida -= new_allocation
                            
                        if alocacao_origens[ponto_mais_proximo] == 0:
                            pontos_sem_capacidade.append(ponto_mais_proximo)
                    
                    
                    if new_allocation > 0:
                        if ponto_mais_proximo in rotas_parent1:
                            rotas_parent1[ponto_mais_proximo][porto] = new_allocation
                        else:
                            rotas_parent1[ponto_mais_proximo] = {porto: new_allocation}
                            
        cromo.lista_adjacencia = rotas_parent1
    
def montar_rotas_faltantes_2(child, parent1, parent2):
    for i, cromo in enumerate(child.cromossomos):
        cromo.set_genes(gene_produtores=parent2.cromossomos[i].gene_produtores,
                        gene_transbordos=parent1.cromossomos[i].gene_transbordos,
                        gene_portos=parent1.cromossomos[i].gene_portos)
        
        rotas_parent1 = parent1.cromossomos[i].lista_adjacencia
        
        alocacao_destinos = cromo.gene_portos.copy()
        alocacao_transbordos = cromo.gene_transbordos.copy()
        alocacao_origens = cromo.gene_produtores.copy()
        
        apagar_rotas_OI_e_OD(rotas_parent1)
        pontos_sem_capacidade = [] 
        for produtor in inp.N:
            if alocacao_origens[produtor] > 0:
                alocacao_a_ser_distribuida = alocacao_origens[produtor]
                while alocacao_a_ser_distribuida > 0:
                    ponto_mais_proximo = find_nearest_neighbor(ponto_referencia=produtor, possiveis_destinos=inp.K + inp.M, 
                                                               pontos_sem_capacidade=pontos_sem_capacidade)
                    
                    if ponto_mais_proximo in inp.K:
                        if alocacao_origens[produtor] <= alocacao_transbordos[ponto_mais_proximo - inp.range_trans]:
                            new_allocation = alocacao_origens[produtor]
                            alocacao_transbordos[ponto_mais_proximo - inp.range_trans] -= new_allocation
                            alocacao_a_ser_distribuida -= new_allocation
                            alocacao_origens[produtor] = 0
                        else:
                            excess = alocacao_origens[produtor] - alocacao_transbordos[ponto_mais_proximo - inp.range_trans]
                            new_allocation = alocacao_origens[produtor] - excess
                            alocacao_transbordos[ponto_mais_proximo - inp.range_trans] -= new_allocation
                            alocacao_origens[produtor] -= new_allocation
                            alocacao_a_ser_distribuida -= new_allocation
                            
                        if alocacao_transbordos[ponto_mais_proximo - inp.range_trans] == 0:
                            pontos_sem_capacidade.append(ponto_mais_proximo)
                    elif ponto_mais_proximo in inp.M:
                        if alocacao_origens[produtor] <= alocacao_destinos[ponto_mais_proximo - inp.range_port]:
                            new_allocation = alocacao_origens[produtor]
                            alocacao_destinos[ponto_mais_proximo - inp.range_port] -= new_allocation
                            alocacao_a_ser_distribuida -= new_allocation
                            alocacao_origens[produtor] = 0
                        else:
                            excess = alocacao_origens[produtor] - alocacao_destinos[ponto_mais_proximo - inp.range_port]
                            new_allocation = alocacao_origens[produtor] - excess
                            alocacao_destinos[ponto_mais_proximo - inp.range_port] -= new_allocation
                            alocacao_origens[produtor] -= new_allocation
                            alocacao_a_ser_distribuida -= new_allocation
                            
                        if alocacao_destinos[ponto_mais_proximo - inp.range_port] == 0:
                            pontos_sem_capacidade.append(ponto_mais_proximo)

                    if new_allocation > 0:
                        if produtor in rotas_parent1:
                            rotas_parent1[produtor][ponto_mais_proximo] = new_allocation
                        else:
                            rotas_parent1[produtor] = {ponto_mais_proximo: new_allocation}
                            
        cromo.lista_adjacencia = rotas_parent1
        
        
# def montar_rotas_faltantes_3(child, parent1, parent2):
#     for i, cromo in enumerate(child.cromossomos):
#         cromo.set_genes(gene_produtores=parent1.cromossomos[i].gene_produtores,
#                         gene_transbordos=parent2.cromossomos[i].gene_transbordos,
#                         gene_portos=parent1.cromossomos[i].gene_portos)
        
#         rotas_parent1 = parent1.cromossomos[i].lista_adjacencia
        
#         alocacao_destinos = cromo.gene_portos.copy()
#         alocacao_transbordos = cromo.gene_transbordos.copy()
#         alocacao_origens = cromo.gene_produtores.copy()
        
#         apagar_rotas_OI_e_ID(rotas_parent1)
#         pontos_sem_capacidade = [] 
#         for transbordo in inp.K:
#             if alocacao_transbordos[transbordo - inp.range_trans] > 0:
#                 alocacao_a_ser_distribuida = alocacao_transbordos[transbordo - inp.range_trans]
#                 while alocacao_a_ser_distribuida > 0:
#                     ponto_mais_proximo = find_nearest_neighbor(ponto_referencia=transbordo, possiveis_destinos=inp.N, 
#                                                                pontos_sem_capacidade=pontos_sem_capacidade)
                    
#                     if ponto_mais_proximo in inp.K:
#                         if alocacao_origens[produtor] <= alocacao_transbordos[ponto_mais_proximo - inp.range_trans]:
#                             new_allocation = alocacao_origens[produtor]
#                             alocacao_transbordos[ponto_mais_proximo - inp.range_trans] -= new_allocation
#                             alocacao_a_ser_distribuida -= new_allocation
#                             alocacao_origens[produtor] = 0
#                         else:
#                             excess = alocacao_origens[produtor] - alocacao_transbordos[ponto_mais_proximo - inp.range_trans]
#                             new_allocation = alocacao_origens[produtor] - excess
#                             alocacao_transbordos[ponto_mais_proximo - inp.range_trans] -= new_allocation
#                             alocacao_origens[produtor] -= new_allocation
#                             alocacao_a_ser_distribuida -= new_allocation
                            
#                         if alocacao_transbordos[ponto_mais_proximo - inp.range_trans] == 0:
#                             pontos_sem_capacidade.append(ponto_mais_proximo)
#                     elif ponto_mais_proximo in inp.M:
#                         if alocacao_origens[produtor] <= alocacao_destinos[ponto_mais_proximo - inp.range_port]:
#                             new_allocation = alocacao_origens[produtor]
#                             alocacao_destinos[ponto_mais_proximo - inp.range_port] -= new_allocation
#                             alocacao_a_ser_distribuida -= new_allocation
#                             alocacao_origens[produtor] = 0
#                         else:
#                             excess = alocacao_origens[produtor] - alocacao_destinos[ponto_mais_proximo - inp.range_port]
#                             new_allocation = alocacao_origens[produtor] - excess
#                             alocacao_destinos[ponto_mais_proximo - inp.range_port] -= new_allocation
#                             alocacao_origens[produtor] -= new_allocation
#                             alocacao_a_ser_distribuida -= new_allocation
                            
#                         if alocacao_destinos[ponto_mais_proximo - inp.range_port] == 0:
#                             pontos_sem_capacidade.append(ponto_mais_proximo)

#                     if new_allocation > 0:
#                         if produtor in rotas_parent1:
#                             rotas_parent1[produtor][ponto_mais_proximo] = new_allocation
#                         else:
#                             rotas_parent1[produtor] = {ponto_mais_proximo: new_allocation}
                            
#         cromo.lista_adjacencia = rotas_parent1
    
        
def crossover_1(parent1, parent2):
    child1 = Individuo(montar_solução_random=False)
    child2 = Individuo(montar_solução_random=False)
    
    montar_rotas_faltantes_1(child1, parent1, parent2)
    montar_rotas_faltantes_1(child2, parent2, parent1)
    
    return child1, child2


def crossover_2(parent1, parent2):
    child1 = Individuo(montar_solução_random=False)
    child2 = Individuo(montar_solução_random=False)
    
    montar_rotas_faltantes_2(child1, parent1, parent2)
    montar_rotas_faltantes_2(child2, parent2, parent1)
    
    return child1, child2

# def crossover_3(parent1, parent2):
#     child1 = Individuo(montar_solução_random=False)
#     child2 = Individuo(montar_solução_random=False)
    
#     montar_rotas_faltantes_3(child1, parent1, parent2)
#     montar_rotas_faltantes_3(child2, parent2, parent1)
    
#     return child1, child2


def crossover(parent1, parent2):
    child1, child2 = crossover_1(parent1, parent2)
    child3, child4 = crossover_2(parent1, parent2)
    return child1, child2, child3, child4


def get_fit(populacao):
    fit = [individuo.valor_fit for individuo in populacao]
    return fit

def update_fit(populacao):
    OF = []
    FIT = []
    for individuo in populacao:
        valor_of = individuo.objective_function()
        OF.append(valor_of)
        FIT.append(individuo.calcular_fit(valor_of=valor_of))
        
    return OF, FIT


def update_population(population, of, fit, n_pop):
    SORT_POSITIONS = np.argsort(of)
    new_population = []
    new_of = []
    new_fit = []
    
    for i in range(n_pop):
        new_population.append(population[SORT_POSITIONS[i]])
        new_of.append(of[SORT_POSITIONS[i]])
        new_fit.append(fit[SORT_POSITIONS[i]])
        
    return new_population, new_of, new_fit


n_iter = 3000
n_pop = 100
populacao = criar_população(n_pop)

of, fit = update_fit(populacao)
# populacao, of, fit = update_population(populacao, of, fit, n_pop)

# Iteration procedure
for it in range(n_iter):
    new_population = []
    for ind in range(n_pop):
        # Selection procedure
        escolha = random()
        if escolha <= 0.3:
            parent1, parent2 = roulette_wheel_selection(populacao=populacao, fit=fit)
        else:
            parent1, parent2 = tournament_selection(fit, populacao)
        # Crossover procedure
        child1, child2, child3, child4 = crossover(parent1=parent1, parent2=parent2)
        # Add in new population
        new_population.append(child1)
        new_population.append(child2)
        new_population.append(child3)
        new_population.append(child4)
    
    new_of, new_fit = update_fit(new_population)
    
    populacao = populacao + new_population
    of = of + new_of
    fit = fit + new_fit
    
    populacao, of, fit = update_population(populacao, of, fit, n_pop)
    print(of[:3])
    print('\n')
    
