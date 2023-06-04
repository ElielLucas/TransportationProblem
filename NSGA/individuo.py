import numpy as np
import random
import defines as inp
from typing import List

def find_nearest_neighbor(ponto_referencia, possiveis_destinos, pontos_sem_capacidade):
        vizinho_mais_proximo = float('inf')
        indice_vizinho_mais_proximo = None

        for i, distancia in enumerate(inp.dist_matrix[ponto_referencia]):
            if i in possiveis_destinos and i not in pontos_sem_capacidade and distancia < vizinho_mais_proximo:
                vizinho_mais_proximo = distancia
                indice_vizinho_mais_proximo = i

        return indice_vizinho_mais_proximo
    
    
def calcular_custo_transporte(gene):
    custo_transporte= 0
    for node_ini, aresta in gene.lista_adjacencia.items():
        for node_fim, custo in aresta.items():
            custo_transporte += custo * inp.dist_matrix[node_ini][node_fim]
    return custo_transporte


def alocar_demanda(provider, target, range_point, provider_allocation,
                   target_point_allocation, target_point_capacity, 
                   total_demanda, cromossomo):
        new_allocation = 0
        if len(range_point) == 1:
            range_provider = 0
            range_target = range_point[0]
        else:
            range_provider = range_point[0]
            range_target = range_point[1]
        if provider_allocation[provider - range_provider] <= target_point_capacity[target - range_target]:
            new_allocation = provider_allocation[provider - range_provider]
            target_point_allocation[target - range_target] += new_allocation
            target_point_capacity[target - range_target] -= new_allocation
            total_demanda -= new_allocation
            provider_allocation[provider - range_provider] = 0
        else:
            excess = provider_allocation[provider - range_provider] - target_point_capacity[target - range_target]
            new_allocation = provider_allocation[provider - range_provider] - excess
            target_point_allocation[target - range_target] += new_allocation
            provider_allocation[provider - range_provider] -= new_allocation
            target_point_capacity[target - range_target] -= new_allocation
            total_demanda -= new_allocation
        
        cromossomo.add_edge(provider, target, new_allocation)
        return target_point_allocation, total_demanda
    
    
class Cromossomo:
    def __init__(self) -> None:
        self.gene_produtores = np.zeros(len(inp.N))
        self.gene_transbordos = np.zeros(len(inp.M))
        self.gene_portos = np.zeros(len(inp.K))
        self.lista_adjacencia = {}

    def set_genes(self, gene_produtores: List[int], gene_transbordos: List[int], gene_portos: List[int]):
        self.gene_produtores = gene_produtores
        self.gene_transbordos = gene_transbordos
        self.gene_portos = gene_portos
        

    def add_edge(self, u: int, v: int, weight: int):
        if u in self.lista_adjacencia:
            self.lista_adjacencia[u][v] = weight
        else:
            self.lista_adjacencia[u] = {v: weight}

     
class Individuo:
    def __init__(self, montar_solução_random: bool) -> None:
        self.produtores = inp.N
        self.portos = inp.M
        self.ferrovias = inp.K
        self.demandas_clientes = inp.demandas_clientes.copy()
        self.cromossomos = [Cromossomo()] * len(self.demandas_clientes)
        
        if montar_solução_random:
            self.montar_solução_random()
    

    def montar_solução_random(self):
        pontos_sem_capacidade = []
        for i, demanda in enumerate(self.demandas_clientes):
            alocacao_transbordos = [0] * len(self.ferrovias)
            alocacao_portos = [0] * len(self.portos)
            alocacao_produtores = self.distribuir_demanda_aleatoriamente_para_produtores(demanda=demanda, ofertas=inp.ofertas, quantidade_produtores=len(self.produtores))
            
            self.distribuir_demanda_de_produtores_para_transbordo_e_portos(gene_origem=alocacao_produtores, gene_intermediario=alocacao_transbordos, 
                                                                           gene_destino=alocacao_portos, capacidade_intermediarios=inp.capacidade_ferrovias, 
                                                                           capacidade_destino=inp.capacidade_portos, pontos_sem_capacidade=pontos_sem_capacidade,
                                                                           origens=self.produtores, intermediarios=self.ferrovias, destinos=self.portos, 
                                                                           cromossomo=self.cromossomos[i])
            self.distribuir_demanda_de_transbordos_para_portos(gene_intermediario=alocacao_transbordos, gene_destino=alocacao_portos, 
                                                               capacidade_destino=inp.capacidade_portos, pontos_sem_capacidade=pontos_sem_capacidade,
                                                               intermediarios=self.ferrovias, destinos=self.portos, cromossomo=self.cromossomos[i])
            
            self.cromossomos[i].set_genes(gene_produtores=alocacao_produtores, 
                                          gene_transbordos=alocacao_transbordos, 
                                          gene_portos=alocacao_portos)


    def distribuir_demanda_aleatoriamente_para_produtores(self, demanda, ofertas, quantidade_produtores):
        vetor = [0] * quantidade_produtores
        demanda_a_ser_distribuida = demanda
        while demanda_a_ser_distribuida > 0:
            for i in range(quantidade_produtores):
                aleatorio = random.randint(0,min(ofertas[i] - vetor[i], demanda_a_ser_distribuida))   
                vetor[i] += aleatorio
                demanda_a_ser_distribuida -= aleatorio

        return vetor


    def distribuir_demanda_de_produtores_para_transbordo_e_portos(self, gene_origem, gene_intermediario, gene_destino, 
                                                                capacidade_intermediarios, capacidade_destino, 
                                                                pontos_sem_capacidade, origens, intermediarios, destinos,
                                                                cromossomo):
        aloc_prod = gene_origem.copy()
        for produtor in origens:
            if aloc_prod[produtor] > 0:
                alocacao_a_ser_distribuida = aloc_prod[produtor]
                while alocacao_a_ser_distribuida > 0:
                    ponto_mais_proximo = find_nearest_neighbor(ponto_referencia=produtor, possiveis_destinos=intermediarios + destinos, 
                                                            pontos_sem_capacidade=pontos_sem_capacidade)
                    if ponto_mais_proximo in intermediarios:
                        gene_intermediario, alocacao_a_ser_distribuida = alocar_demanda(provider=produtor, target=ponto_mais_proximo, range_point = [inp.range_trans],
                                                                                        provider_allocation=aloc_prod, target_point_allocation=gene_intermediario, 
                                                                                        target_point_capacity=capacidade_intermediarios, total_demanda=alocacao_a_ser_distribuida,
                                                                                        cromossomo=cromossomo)
                        if capacidade_intermediarios[ponto_mais_proximo - inp.range_trans] == 0:
                            pontos_sem_capacidade.append(ponto_mais_proximo)
                    else:
                        gene_destino, alocacao_a_ser_distribuida = alocar_demanda(provider=produtor, target=ponto_mais_proximo,  range_point=[inp.range_port],
                                                                                  provider_allocation=aloc_prod, target_point_allocation=gene_destino, 
                                                                                  target_point_capacity=capacidade_destino, total_demanda=alocacao_a_ser_distribuida,
                                                                                  cromossomo=cromossomo)
                        if capacidade_destino[ponto_mais_proximo - inp.range_port] == 0:
                            pontos_sem_capacidade.append(ponto_mais_proximo)
                            
                            
    def distribuir_demanda_de_transbordos_para_portos(self, gene_intermediario, gene_destino, 
                                                      capacidade_destino, pontos_sem_capacidade,
                                                      intermediarios, destinos, cromossomo):
        
        aloc_trans = gene_intermediario.copy()
        for transbordo in intermediarios:
            if aloc_trans[transbordo - inp.range_trans] > 0:
                alocacao_a_ser_distribuida = aloc_trans[transbordo - inp.range_trans]
                while alocacao_a_ser_distribuida > 0:
                    ponto_mais_proximo = find_nearest_neighbor(ponto_referencia=transbordo, possiveis_destinos=destinos, 
                                                               pontos_sem_capacidade=pontos_sem_capacidade)
                    gene_destino, alocacao_a_ser_distribuida = alocar_demanda(provider=transbordo, target=ponto_mais_proximo, range_point=[inp.range_trans, inp.range_port],
                                                                              provider_allocation=aloc_trans, target_point_allocation=gene_destino, 
                                                                              target_point_capacity=capacidade_destino, total_demanda=alocacao_a_ser_distribuida,
                                                                              cromossomo=cromossomo)
                    if capacidade_destino[ponto_mais_proximo - inp.range_port] == 0:
                        pontos_sem_capacidade.append(ponto_mais_proximo)
                    
        
    def objective_function(self):
        custo_total = 0
        for i in range(len(self.demandas_clientes)):
            custo_total += calcular_custo_transporte(gene=self.cromossomos[i])
        return custo_total

        

        
        
        
        
 
        