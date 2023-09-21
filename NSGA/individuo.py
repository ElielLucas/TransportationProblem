import numpy as np
import random
# from defines import Defines
import input as inp
from typing import List, Dict, DefaultDict, Set
from collections import defaultdict    
    
class Cromossomo:
    def __init__(self) -> None:
        self.gene_produtores = np.zeros_like(inp.N)
        self.gene_transbordos = np.zeros_like(inp.M)
        self.gene_portos = np.zeros_like(inp.K)
        self.lista_adjacencia: DefaultDict[int, Dict[int, int]] = defaultdict(dict)

    def set_genes(self, gene_produtores, gene_transbordos, gene_portos) -> None:
        self.gene_produtores = gene_produtores
        self.gene_transbordos = gene_transbordos
        self.gene_portos = gene_portos

    def add_edge(self, u: int, v: int, weight: int) -> None:
        self.lista_adjacencia[u][v] = weight

     
class  Individuo:
    def __init__(self, montar_solução_random: bool) -> None:
        self.produtores = inp.N
        self.portos = inp.M
        self.ferrovias = inp.K
        self.demandas_clientes = inp.demandas.copy()
        self.cromossomos = []
        self.cap_destino = inp.CP.copy()
        self.cap_trans = inp.CF.copy()
        self.ofert_prod = inp.ofertas.copy()
        
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        self.features = None
        
        self.of = []
        self.fit = []
        for _ in range(len(self.demandas_clientes)):
            self.cromossomos.append(Cromossomo())
        
        if montar_solução_random:
            self.montar_solução_random() 
            self.calculate_objectives()

    
    def __lt__(self,other):
        return (self.of[0] < other.of[0] and self.of[1] <= other.of[1]) or (self.of[0] <= other.of[0] and self.of[1] < other.of[1])
    
    def montar_solução_random(self):
        pontos_sem_capacidade: Set[int] = set()
        for i, demanda in enumerate(self.demandas_clientes):
            alocacao_transbordos = [0] * len(self.ferrovias)
            alocacao_portos = [0] * len(self.portos)
            alocacao_produtores = self.distribuir_demanda_aleatoriamente_para_produtores(demanda=demanda, ofertas=self.ofert_prod, quantidade_produtores=len(self.produtores))
            self.distribuir_demanda_de_produtores_para_transbordo_e_portos(gene_origem=alocacao_produtores, gene_intermediario=alocacao_transbordos, 
                                                                           gene_destino=alocacao_portos, capacidade_intermediarios=self.cap_trans, 
                                                                           capacidade_destino=self.cap_destino, pontos_sem_capacidade=pontos_sem_capacidade,
                                                                           origens=self.produtores, intermediarios=self.ferrovias, destinos=self.portos, 
                                                                           cromossomo=self.cromossomos[i])
            self.distribuir_demanda_de_transbordos_para_portos(gene_intermediario=alocacao_transbordos, gene_destino=alocacao_portos, 
                                                               capacidade_destino=self.cap_destino, pontos_sem_capacidade=pontos_sem_capacidade,
                                                               intermediarios=self.ferrovias, destinos=self.portos, cromossomo=self.cromossomos[i])
            
            self.cromossomos[i].set_genes(gene_produtores=alocacao_produtores.copy(), 
                                          gene_transbordos=alocacao_transbordos.copy(), 
                                          gene_portos=alocacao_portos.copy())


    def distribuir_demanda_aleatoriamente_para_produtores(self, demanda, ofertas, quantidade_produtores):
        vetor = np.zeros(quantidade_produtores)
        while demanda > 0:
            produtor = random.choice(np.where(ofertas - vetor > 0)[0])
            aleatorio = random.randint(0, int(min(ofertas[produtor] - vetor[int(produtor)], demanda)))   
            vetor[produtor] += aleatorio
            demanda -= aleatorio
        return vetor

    
    def distribuir_demanda_de_produtores_para_transbordo_e_portos(self, gene_origem, gene_intermediario, gene_destino, 
                                                                 capacidade_intermediarios, capacidade_destino, 
                                                                 pontos_sem_capacidade, origens, intermediarios, destinos,
                                                                 cromossomo):
        aloc_prod = gene_origem.copy()
        for produtor in origens:
            alocacao_a_ser_distribuida = aloc_prod[produtor]
            while alocacao_a_ser_distribuida > 0:
                ponto_mais_proximo = self.find_nearest_neighbor(ponto_referencia=produtor, 
                                                        possiveis_destinos=intermediarios + destinos, 
                                                        pontos_sem_capacidade=pontos_sem_capacidade)
                if ponto_mais_proximo in intermediarios:
                    demanda_alocar = min(alocacao_a_ser_distribuida, capacidade_intermediarios[ponto_mais_proximo - inp.range_trans])
                    if demanda_alocar > 0:
                        gene_intermediario, alocacao_a_ser_distribuida = self.alocar_demanda(provider=produtor, 
                                                                                        target=ponto_mais_proximo, 
                                                                                        range_point=[inp.range_trans],
                                                                                        provider_allocation=aloc_prod, 
                                                                                        target_point_allocation=gene_intermediario, 
                                                                                        target_point_capacity=capacidade_intermediarios, 
                                                                                        total_demanda=alocacao_a_ser_distribuida,
                                                                                        cromossomo=cromossomo)
                    else:
                        pontos_sem_capacidade.add(ponto_mais_proximo)
                else:
                    demanda_alocar = min(alocacao_a_ser_distribuida, capacidade_destino[ponto_mais_proximo - inp.range_port])
                    if demanda_alocar > 0:
                        gene_destino, alocacao_a_ser_distribuida = self.alocar_demanda(provider=produtor, 
                                                                                  target=ponto_mais_proximo,  
                                                                                  range_point=[inp.range_port],
                                                                                  provider_allocation=aloc_prod, 
                                                                                  target_point_allocation=gene_destino, 
                                                                                  target_point_capacity=capacidade_destino, 
                                                                                  total_demanda=alocacao_a_ser_distribuida,
                                                                                  cromossomo=cromossomo)
                    else:
                        pontos_sem_capacidade.add(ponto_mais_proximo)
                            
                            
    def distribuir_demanda_de_transbordos_para_portos(self, gene_intermediario, gene_destino, 
                                                      capacidade_destino, pontos_sem_capacidade,
                                                      intermediarios, destinos, cromossomo):
        
        aloc_trans = gene_intermediario.copy()
        for transbordo in intermediarios:
            if aloc_trans[transbordo - inp.range_trans] > 0:
                alocacao_a_ser_distribuida = aloc_trans[transbordo - inp.range_trans]
                while alocacao_a_ser_distribuida > 0:
                    ponto_mais_proximo = self.find_nearest_neighbor(ponto_referencia=transbordo, possiveis_destinos=destinos, 
                                                               pontos_sem_capacidade=pontos_sem_capacidade)
                    gene_destino, alocacao_a_ser_distribuida = self.alocar_demanda(provider=transbordo, target=ponto_mais_proximo, range_point=[inp.range_trans, inp.range_port],
                                                                              provider_allocation=aloc_trans, target_point_allocation=gene_destino, 
                                                                              target_point_capacity=capacidade_destino, total_demanda=alocacao_a_ser_distribuida,
                                                                              cromossomo=cromossomo)
                    if capacidade_destino[ponto_mais_proximo - inp.range_port] == 0:
                        pontos_sem_capacidade.add(ponto_mais_proximo)
    
    
    # Check if individual1 dominates individual2
    def dominates(self, other_individual):
        and_condition = True
        or_condition = False
        for first, second in zip(self.of, other_individual.of):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return (and_condition and or_condition)
    
    
    def calculate_objectives(self):
        self.of = self.objective_function()
        self.fit = self.calculate_fit(self.of)
    
    def objective_function(self):
        custo_total = 0
        emissao_total = 0
        for i in range(len(self.demandas_clientes)):
            custo, emissao = self.calcular_custo_e_emissao_transporte(gene=self.cromossomos[i])
            custo_total += custo
            emissao_total += emissao
            
        return [custo_total, emissao_total]


    def calculate_fit(self, of):
        of_custo, of_emissao = of
        if of_custo >= 0:
            fit_custo = 1 / (1 + of_custo)
        elif of_custo < 0:
            fit_custo = 1 + abs(of_custo)
            
        if of_emissao >= 0:
            fit_emissao = 1 / (1 + of_emissao)
        elif of_emissao < 0:
            fit_emissao = 1 + abs(of_emissao)

        return [fit_custo, fit_emissao]
    
    def find_nearest_neighbor(self, ponto_referencia, possiveis_destinos, pontos_sem_capacidade):
        pontos_sem_capacidade = set(pontos_sem_capacidade)
        vizinho_mais_proximo = float('inf')
        indice_vizinho_mais_proximo = None
        for i, distancia in enumerate(inp.dist_matrix[ponto_referencia]):
            if i in possiveis_destinos and i not in pontos_sem_capacidade and distancia < vizinho_mais_proximo:
                vizinho_mais_proximo = distancia
                indice_vizinho_mais_proximo = i

        return indice_vizinho_mais_proximo
        

    def calcular_custo_e_emissao_transporte(self, gene):
        N = set(inp.N)
        K = set(inp.K)
        M = set(inp.M)

        custo_transporte = 0
        emissao_transporte = 0
        for node_ini, aresta in gene.lista_adjacencia.items():
            for node_fim, qtd_transportada in aresta.items():
                if (node_ini in N and node_fim in K) or (node_ini in N and node_fim in M):
                    custo_modal = inp.cr
                    emissao_modal = inp.er
                else:
                    custo_modal = inp.cf
                    emissao_modal = inp.ef

                custo_transporte += (qtd_transportada * inp.dist_matrix[node_ini][node_fim] * custo_modal)
                emissao_transporte += qtd_transportada * inp.tempo_matrix[node_ini, node_fim] * emissao_modal
                # inp.tempo_matrix[node_ini][node_fim]
        return [custo_transporte, emissao_transporte]


    def alocar_demanda(self, provider, target, range_point, provider_allocation,
                      target_point_allocation, target_point_capacity, 
                      total_demanda, cromossomo):
        # Pre-calcule valores comumente referenciados
        range_provider = 0 if len(range_point) == 1 else range_point[0]
        range_target = range_point[0] if len(range_point) == 1 else range_point[1]

        provider_index = provider - range_provider
        target_index = target - range_target

        # Determine a nova alocação baseada na capacidade e na alocação do fornecedor
        new_allocation = min(provider_allocation[provider_index], target_point_capacity[target_index])

        # Atualize a alocação e capacidade
        provider_allocation[provider_index] -= new_allocation
        target_point_allocation[target_index] += new_allocation
        target_point_capacity[target_index] -= new_allocation
        total_demanda -= new_allocation

        # Adicione a borda ao cromossomo
        cromossomo.add_edge(provider, target, new_allocation)

        return target_point_allocation, total_demanda

            

            
            
            
            
    
            