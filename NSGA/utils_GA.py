from individuo import Individuo, calcular_custo_transporte, find_nearest_neighbor, alocar_demanda
from random import random, choice, randint, randrange, sample
import numpy as np
import defines as inp
from typing import List
import time


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
    for node_ini in (inp.N + inp.K):
        if node_ini in rotas:
            for node_fim in list(rotas[node_ini]):
                if node_fim in inp.M:
                    del rotas[node_ini][node_fim]


def apagar_rotas_OI_e_OD(rotas):
    for node in inp.N:
        if node in rotas:
            del rotas[node]
            

def apagar_rotas_OI_e_ID(rotas):
    for node_ini in (inp.N + inp.K):
        if node_ini in rotas:
            for node_fim in list(rotas[node_ini]):
                if node_fim in (inp.K + inp.M):
                    del rotas[node_ini][node_fim]
            
     
def montar_rotas_faltantes_1(child: Individuo, parent1, parent2):
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
            
        apagar_rotas_OD(rotas_parent1)
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
    
def montar_rotas_faltantes_2(child, parent1, parent2):
    K = set(inp.K)
    M = set(inp.M)
    for i, cromo in enumerate(child.cromossomos):
        cromo.set_genes(gene_produtores=parent2.cromossomos[i].gene_produtores,
                        gene_transbordos=parent1.cromossomos[i].gene_transbordos,
                        gene_portos=parent1.cromossomos[i].gene_portos)
        
        rotas_parent1 = parent1.cromossomos[i].lista_adjacencia
        
        alocacao_destinos = cromo.gene_portos.copy()
        alocacao_transbordos = cromo.gene_transbordos.copy()
        alocacao_origens = cromo.gene_produtores.copy()
        
        apagar_rotas_OI_e_OD(rotas_parent1)
        pontos_disponiveis = list(K | M)
        for produtor in inp.N:
            if alocacao_origens[produtor] > 0:
                alocacao_a_ser_distribuida = alocacao_origens[produtor]
                while alocacao_a_ser_distribuida > 0:
                    ponto_mais_proximo = choice(pontos_disponiveis)

                    if ponto_mais_proximo in K:
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
                            pontos_disponiveis.remove(ponto_mais_proximo)
                    elif ponto_mais_proximo in M:
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
                            pontos_disponiveis.remove(ponto_mais_proximo)
                    
                    # ponto_mais_proximo = choice(pontos_disponiveis)
                    # if ponto_mais_proximo in K:
                    #     alocacao_ponto = alocacao_transbordos[ponto_mais_proximo - inp.range_trans]
                    # elif ponto_mais_proximo in M:
                    #     alocacao_ponto = alocacao_destinos[ponto_mais_proximo - inp.range_port]

                    # if alocacao_origens[produtor] <= alocacao_ponto:
                    #     new_allocation = alocacao_origens[produtor]
                    # else:
                    #     excess = alocacao_origens[produtor] - alocacao_ponto
                    #     new_allocation = alocacao_origens[produtor] - excess
                        
                    # if ponto_mais_proximo in K:
                    #     alocacao_transbordos[ponto_mais_proximo - inp.range_trans] -= new_allocation
                    # elif ponto_mais_proximo in M:
                    #     alocacao_destinos[ponto_mais_proximo - inp.range_port] -= new_allocation

                    # alocacao_a_ser_distribuida -= new_allocation
                    # alocacao_destinos[ponto_mais_proximo - inp.range_port] -= new_allocation

                    # if alocacao_ponto == 0:
                    #     pontos_disponiveis.remove(ponto_mais_proximo)

                    if new_allocation > 0:
                        rotas_parent1[produtor][ponto_mais_proximo] = new_allocation
                            
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
#         if sum(alocacao_transbordos) > 0:
#             apagar_rotas_OI_e_ID(rotas_parent1)
#         pontos_sem_capacidade = [] 
#         for transbordo in inp.K:
#             if alocacao_transbordos[transbordo - inp.range_trans] > 0:
#                 alocacao_a_ser_distribuida = alocacao_transbordos[transbordo - inp.range_trans]
#                 while alocacao_a_ser_distribuida > 0:
#                     ponto_mais_proximo = find_nearest_neighbor(ponto_referencia=transbordo, possiveis_destinos=inp.N, 
#                                                                pontos_sem_capacidade=pontos_sem_capacidade)
                    
#                     if alocacao_transbordos[transbordo - inp.range_trans] <= alocacao_origens[ponto_mais_proximo]:
#                         new_allocation = alocacao_transbordos[transbordo - inp.range_trans]
#                         alocacao_origens[ponto_mais_proximo] -= new_allocation
#                         alocacao_a_ser_distribuida -= new_allocation
#                         alocacao_transbordos[transbordo - inp.range_trans] = 0
#                     else:
#                         excess = alocacao_transbordos[transbordo - inp.range_trans] - alocacao_origens[ponto_mais_proximo]
#                         new_allocation = alocacao_transbordos[transbordo - inp.range_trans] - excess
#                         alocacao_origens[ponto_mais_proximo] -= new_allocation
#                         alocacao_transbordos[transbordo - inp.range_trans] -= new_allocation
#                         alocacao_a_ser_distribuida -= new_allocation

                        
#                     if alocacao_origens[ponto_mais_proximo] == 0:
#                         pontos_sem_capacidade.append(ponto_mais_proximo)

#                     if new_allocation > 0:
#                         if ponto_mais_proximo in rotas_parent1:
#                             rotas_parent1[ponto_mais_proximo][transbordo] = new_allocation
#                         else:
#                             rotas_parent1[ponto_mais_proximo] = {transbordo: new_allocation}
                            
                            
#         for transbordo in inp.K:
#             if alocacao_transbordos[transbordo - inp.range_trans] > 0:
#                 alocacao_a_ser_distribuida = alocacao_transbordos[transbordo - inp.range_trans]
#                 while alocacao_a_ser_distribuida > 0:
#                     ponto_mais_proximo = find_nearest_neighbor(ponto_referencia=transbordo, possiveis_destinos=inp.M, 
#                                                                pontos_sem_capacidade=pontos_sem_capacidade)
                    
#                     if alocacao_transbordos[transbordo - inp.range_trans] <= alocacao_destinos[ponto_mais_proximo - inp.range_port]:
#                         new_allocation = alocacao_transbordos[transbordo - inp.range_trans]
#                         alocacao_destinos[ponto_mais_proximo - inp.range_port] -= new_allocation
#                         alocacao_a_ser_distribuida -= new_allocation
#                         alocacao_transbordos[transbordo - inp.range_trans] = 0
#                     else:
#                         excess = alocacao_transbordos[transbordo - inp.range_trans] - alocacao_destinos[ponto_mais_proximo - inp.range_port]
#                         new_allocation = alocacao_transbordos[transbordo - inp.range_trans] - excess
#                         alocacao_destinos[ponto_mais_proximo - inp.range_port] -= new_allocation
#                         alocacao_transbordos[transbordo - inp.range_trans] -= new_allocation
#                         alocacao_a_ser_distribuida -= new_allocation

                        
#                     if alocacao_origens[ponto_mais_proximo] == 0:
#                         pontos_sem_capacidade.append(ponto_mais_proximo)

#                     if new_allocation > 0:
#                         if transbordo in rotas_parent1:
#                             rotas_parent1[transbordo][ponto_mais_proximo] = new_allocation
#                         else:
#                             rotas_parent1[transbordo] = {ponto_mais_proximo: new_allocation}
                            
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
    # return crossover_2(parent1, parent2)
    escolha = choice([1])
    if escolha == 1:
        return crossover_1(parent1, parent2)
    elif escolha == 2:
        return crossover_2(parent1, parent2)
    # else:
    #     return crossover_3(parent1, parent2)
    
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

