from individuo import Individuo, calcular_custo_transporte, find_nearest_neighbor, alocar_demanda
from random import random, choice, randint, randrange, sample
import numpy as np
import defines as inp
from typing import List


def criar_população(tamanho_populacao: int):
    return [Individuo(montar_solução_random=True) for _ in range(tamanho_populacao)]


def objective_function(cromossomo):
    custo_total = 0
    for origem in cromossomo.lista_adjacencia:
        for destino in cromossomo.lista_adjacencia[origem]:
            # o custo é a distância multiplicada pela quantidade de soja a ser transportada
            custo_total += cromossomo.lista_adjacencia[origem][destino] * inp.dist_matrix[origem][destino]
    return custo_total


def fit_value(objective_function_value):
    if objective_function_value >= 0:
        fit_value = 1 / (1 + objective_function_value)
    elif objective_function_value < 0:
        fit_value = 1 + abs(objective_function_value)
    return fit_value
        
        
def roulette_wheel_selection(fit, n_pop):
    ids_individuos = np.linspace(0, n_pop, n_pop, endpoint = False)
    sum_fit = sum(fit)
    prob = []
    for i in range(n_pop):
        prob.append(fit[i] / sum_fit)

    ids_individuos = np.random.choice(ids_individuos, 2, replace = False, p = prob)
    return (int(ids_individuos[0]), int(ids_individuos[1]))       

def apagar_rotas_que_vao_para_portos(rotas):
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
        
def montar_rotas_faltantes(child, parent1, parent2):
    
    for i, cromo in enumerate(child.cromossomos):
        cromo.set_genes(gene_produtores=parent1.cromossomos[i].gene_produtores,
                                        gene_transbordos=parent1.cromossomos[i].gene_transbordos,
                                        gene_portos=parent2.cromossomos[i].gene_portos)
        
        rotas_parent1 = parent1.cromossomos[0].lista_adjacencia
        
        alocacao_destinos = cromo.gene_portos.copy()
        alocacao_transbordos = cromo.gene_transbordos.copy()
        alocacao_origens = [0] * len(inp.N)
        
        # Passa os pesos das arestas para um vetor de origens que será distribuído novamente.
        for node_ini, aresta in rotas_parent1.items():
            for node_fim, custo in aresta.items():
                if node_ini in inp.N and node_fim in inp.M:
                    alocacao_origens[node_ini] += custo
                    
        apagar_rotas_que_vao_para_portos(rotas_parent1)
        
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
    
        
def crossover_1(parent1, parent2):
    child1 = Individuo(montar_solução_random=False)
    child2 = Individuo(montar_solução_random=False)
    
    montar_rotas_faltantes(child1, parent1, parent2)
    montar_rotas_faltantes(child2, parent2, parent1)
    
    return child1, child2
    
    
    
        


    
    
    
    
    

# def local_search(individuo):
#     for cromossomo in individuo.cromossomos:
#         improved = True
#         breakpoint()
#         while improved:
#             improved = False
#             edges = list(cromossomo.lista_adjacencia.keys())

#             for i in range(len(edges)):
#                 for j in range(i + 1, len(edges)):
#                     u1, v1 = edges[i]
#                     u2, v2 = edges[j]

#                     # Armazena temporariamente os pesos das arestas a serem trocadas
#                     peso1 = cromossomo.lista_adjacencia[u1][v1]
#                     peso2 = cromossomo.lista_adjacencia[u2][v2]

#                     # Calcula o custo antes e depois da troca
#                     custo_atual = calcular_custo_transporte(gene=cromossomo)
#                     cromossomo.lista_adjacencia[u1][v1] = peso2
#                     cromossomo.lista_adjacencia[u2][v2] = peso1
#                     custo_apos_troca = calcular_custo_transporte(gene=cromossomo)

#                     # Se a troca resultar em melhoria, mantém a alteração
#                     if custo_apos_troca < custo_atual:
#                         improved = True

#                     # Reverte as alterações caso não haja melhoria
#                     else:
#                         cromossomo.lista_adjacencia[u1][v1] = peso1
#                         cromossomo.lista_adjacencia[u2][v2] = peso2

#     return individuo



def update_fit(populacao):
    OF = [individuo.objective_function() for individuo in populacao]
    FIT = [fit_value(c) for c in OF] 
    
    return OF, FIT   



n_iter = 10
n_pop = 10
populacao = criar_população(n_pop)
OF, FIT = update_fit(populacao=populacao)


# Iteration procedure
for it in range(n_iter):
    new_population = []
    for ind in range(n_pop):
        # Selection procedure
        parent1_index, parent2_index = roulette_wheel_selection(FIT, len(populacao))
        # Crossover procedure
        child1, child2 = crossover_1(parent_1=populacao[parent1_index[0]], parent_2=populacao[parent2_index[1]])
        # Add in new population
        new_population.append(child1)
        new_population.append(child2)
        
       
    new_of, new_fit = update_fit(new_population)
