from utils_GA import NSGA2Utils
from utils_GA import Individuo
from random import random, choice, randint, randrange, sample, sample
import matplotlib.pyplot as plt
from tqdm import tqdm
from random import random
from math import sqrt
import pandas as pd
import numpy as np
import time 

grande_frente_pareto = []
geracao = 0
menor_custo_frente = 1000000000000.0
menor_emissao_frente = 1000000000000.0
taxa_mutacao = 0.5
class Evolution:
    def __init__(self):
        self.taxa_cruzamento = 0.8
        self.taxa_mutacao = 0.05
        self.tamanho_populacao = 80
        self.populacao = None
        self.ranks = None
        self.crowding_distance = None
        self.melhor_individuo = None
        self.custo_medio =0
        self.emissao_media = 0
        self.k = [1,0.5,1,0.5]
        self.rank_medio = 0.0
        self.melhor_rank = 10000
        self.frente = None
        
        self.utils = NSGA2Utils(num_of_individuals=self.tamanho_populacao)
        
    def create_initial_population(self):
        global geracao
        print('gerando populacao')
        self.populacao = []
        for i in range(self.tamanho_populacao):
            new_indiv = Individuo(montar_solução_random=True)
            self.populacao.append(new_indiv)
            self.insere_na_frente(new_indiv)
            for j in range(len(grande_frente_pareto)):
                print('(',grande_frente_pareto[j].of[0],'|',grande_frente_pareto[j].of[1],')',end=',')
            print('')
            if len(grande_frente_pareto) > 1:
                self.plot_frente_de_pareto(str(geracao))
            print('gerados',i,'cromossomos')
        print('Populacao gerada')
        
    def non_dominated_pareto_sort(self):
        self.ranks = [1 for i in range(len(self.populacao))]
        vis = [0 for i in range(len(self.populacao))]
        r = 1
        while True:
            qt = [0 for i in range(len(self.populacao))]
            for x in range(len(self.populacao)):
                if vis[x] == 1:
                    continue
                for y in range(len(self.populacao)):
                    if vis[y] == 1:
                        continue
                    if self.populacao[x] < self.populacao[y]:
                        qt[y] +=1
            para = True
            for i in range(len(self.populacao)):
                if qt[i] == 0 and vis[i]==0:
                    self.ranks[i] = r
                    vis[i]=1
                    para = False
            if para == True:
                break
            r+=1
        self.frente = []
        for i in range(len(self.populacao)):
            if self.ranks[i] == 1:
                self.frente.append(self.populacao[i])
                
    def crowding(self):
        vet_min = [100000000000.0,100000000000.0]
        vet_max = [0.0,0.0]
        for i in range(len(self.populacao)):
            vet_min[0] = min(vet_min[0],self.populacao[i].of[0])
            vet_min[1] = min(vet_min[1],self.populacao[i].of[1])
            vet_max[0] = max(vet_max[0],self.populacao[i].of[0])
            vet_max[1] = max(vet_max[1], self.populacao[i].of[1])
            
        distance = [[0.0 for j in range(len(self.populacao))] for i in range(len(self.populacao))]
        
        for i in range(len(self.populacao)):
            for j in range(len(self.populacao)):
                distance[i][j] = sqrt(float((self.populacao[i].of[0]-self.populacao[j].of[0])*(self.populacao[i].of[0]-self.populacao[j].of[0]) + (self.populacao[i].of[1]-self.populacao[j].of[1])*(self.populacao[i].of[1]-self.populacao[j].of[1])))
                
    
        self.crowding_distance = [0.0 for i in range(len(self.populacao))]
        
        for i in range(len(self.populacao)):
            pos_primeiro = i
            distancia_primeiro = 0.0
            for j in range(len(self.populacao)):
                if self.ranks[i] != self.ranks[j]:
                    continue
                if distance[i][j] > distancia_primeiro:
                    distancia_primeiro = distance[i][j]
                    pos_primeiro = j
                    
            pos_segundo = i
            distancia_segundo = 0.0
            for j in range(len(self.populacao)):
                if self.ranks[i] != self.ranks[j]:
                    continue
                if j == pos_primeiro:
                    continue
                if distance[i][j] > distancia_segundo:
                    distancia_segundo = distance[i][j]
                    pos_segundo = j
                    
            self.crowding_distance[i] = abs(self.populacao[pos_primeiro].of[0] - self.populacao[pos_segundo].of[0])/max((vet_max[0] - vet_min[0]),0.1)+abs(self.populacao[pos_primeiro].of[1] - self.populacao[pos_segundo].of[1])/max((vet_max[1] - vet_min[1]),0.1)
    
    def selection(self):
        populacao = []
        vet_idx = [i for i in range(len(self.populacao))]
        while len(populacao) < self.tamanho_populacao:
            pos = self.tournament_selection(vet_idx)
            populacao.append(self.populacao[vet_idx[pos]])
            vet_idx.pop(pos)
        self.populacao = [] + populacao
        print('Seleção realizada')
                
    def tournament(self,adv=-1):
        lim = len(self.populacao)
        ret = randint(0,lim-1)
        for _ in range(0,3):
            other = randint(0,lim-1)
            while other == adv or other == ret:
                other = randint(0,lim-1)
            if self.populacao[other] < self.populacao[ret]:
                ret = other
        return ret
    
    def tournament_selection(self,vet_idx):
        if len(vet_idx) == 1:
            return 0
        tam = len(vet_idx)
        pos = randint(0,tam-1)
        pos1 = randint(0,tam-1)
        if self.ranks[vet_idx[pos1]] < self.ranks[vet_idx[pos]] or (self.ranks[vet_idx[pos]] == self.ranks[vet_idx[pos1]] and self.crowding_distance[vet_idx[pos1]] > self.crowding_distance[vet_idx[pos]]):
            pos = pos1
        return pos
    
    def aux_cross(self, parent1, parent2):
        child1 = Individuo(montar_solução_random=False)
        child2 = Individuo(montar_solução_random=False)
        self.utils.montar_rotas_faltantes_1(child1, parent1, parent2)
        self.utils.montar_rotas_faltantes_1(child2, parent2, parent1)
        return child1, child2
        
    def crossover(self):
        prob = float(randint(1,100))/100.0
        qtd = int(len(self.populacao)/2)
        prole = []
        while qtd>0:
            parent1 = self.tournament()
            parent2 = self.tournament(adv = parent1)
            if prob <= self.probabilidade_crossover(parent1,parent2):                
                if random() <= 0.6:  
                    indiv_aleatorio = Individuo(montar_solução_random=True)
                    if choice([0, 1]) == 0:
                        child1, child2 = self.aux_cross(parent1=self.populacao[parent1], parent2=indiv_aleatorio)
                    else:
                        child1, child2 = self.aux_cross(parent1=self.populacao[parent2], parent2=indiv_aleatorio)
                else:
                    child1, child2 = self.aux_cross(parent1=self.populacao[parent1], parent2=self.populacao[parent2])
    
                child1.calculate_objectives()
                child2.calculate_objectives()
                prole.append(child1)
                prole.append(child2)
                self.insere_na_frente(child1)
                self.insere_na_frente(child2)
            qtd-=1
        self.populacao += prole
        
    def probabilidade_crossover(self,idx1,idx2):
        idx = idx1
        if(self.ranks[idx2] < self.ranks[idx1]):
            idx = idx2
        if(self.ranks[idx] > self.rank_medio) and self.melhor_rank < self.rank_medio:
            return (self.rank_medio - self.melhor_rank)/(self.rank_medio - self.melhor_rank)
        return 1.0
    
    def mutate(self):
        for e in range(len(self.populacao)):
            p = float(randint(1, 100))/100.0
            if p  <= self.probabilidade_mutacao(e):
                new_indiv = Individuo(montar_solução_random=True)
                self.populacao[e] = new_indiv
                self.insere_na_frente(new_indiv)
        print('Mutação realizada')
    
    def probabilidade_mutacao(self, idx):
        if self.ranks[idx] <= self.rank_medio and self.melhor_rank < self.rank_medio:
            return 0.5*((float(self.ranks[idx]) - float(self.melhor_rank))/(float(self.rank_medio) - float(self.melhor_rank)))
        return 0.5
    
    def calcula_dados(self):
        self.custo_medio = 0.0
        self.emissao_media = 0.0
        self.rank_medio = 0.0
        for i in range(len(self.populacao)):
            self.custo_medio += float(self.populacao[i].of[0])
            self.emissao_media += float(self.populacao[i].of[1])
            self.rank_medio += self.ranks[i]
            self.melhor_rank = min(self.melhor_rank,self.ranks[i])
        self.custo_medio/=float(len(self.populacao))
        self.emissao_media/=float(len(self.populacao))
        self.rank_medio/=float(len(self.populacao))
        
    def insere_na_frente(self, individuo):
        global grande_frente_pareto
        global menor_custo_frente
        global menor_emissao_frente


        if len(grande_frente_pareto) == 0:
            grande_frente_pareto.append(individuo)
            menor_custo_frente = individuo.of[0]
            menor_emissao_frente = individuo.of[1]
            return

        if (individuo.of[0] < menor_custo_frente and individuo.of[1] <= menor_emissao_frente) or (individuo.of[0] <= menor_custo_frente and individuo.of[1] < menor_emissao_frente):
            frente_pareto = []
            frente_pareto.append(individuo)
            menor_custo_frente = individuo.of[0]
            menor_emissao_frente = individuo.of[1]
            return

        coloca = True
        nova_frente = [individuo]
        for i in range(len(grande_frente_pareto)):
            if (individuo.of[0] == grande_frente_pareto[i].of[0] and individuo.of[1] == grande_frente_pareto[i].of[1]) or ((grande_frente_pareto[i].of[0] < individuo.of[0] and grande_frente_pareto[i].of[1] <= individuo.of[1]) or (grande_frente_pareto[i].of[0] <= individuo.of[0] and grande_frente_pareto[i].of[1] < individuo.of[1])):
                coloca = False
                break
            if (individuo.of[0] < grande_frente_pareto[i].of[0] and individuo.of[1] <= grande_frente_pareto[i].of[1]) or (individuo.of[0] <= grande_frente_pareto[i].of[0] and individuo.of[1] < grande_frente_pareto[i].of[1]):
                continue
            nova_frente.append(grande_frente_pareto[i])
        if coloca:
            grande_frente_pareto=nova_frente
            menor_custo_frente= min(individuo.of[0], menor_custo_frente)
            menor_emissao_frente = min(menor_emissao_frente, individuo.of[0])
            
            
    def plot_frente_de_pareto(self, geracao):
        global grande_frente_pareto
        custo_frente = np.array([grande_frente_pareto[i].of[0] for i in range(len(grande_frente_pareto))])
        emissao_frente = np.array([grande_frente_pareto[i].of[1] for i in range(len(grande_frente_pareto))])
        custo = np.array([self.populacao[i].of[0] for i in range(len(self.populacao))])
        emissao = np.array([self.populacao[i].of[1] for i in range(len(self.populacao))])
        plt.scatter(emissao,custo,c=np.array(['blue' for i in range(len(self.populacao))]),label='Outras soluções')
        plt.scatter(emissao_frente, custo_frente, c=np.array(['red' for i in range(len(grande_frente_pareto))]),label='Frente de pareto')
        plt.xlabel('Emissão de CO2')
        plt.ylabel('Custo do transporte')
        plt.title('ANSGA II - Geração '+geracao)
        plt.legend()
        caminho = 'Figuras/' + 'Geração('+str(geracao)+').png'
        plt.savefig(caminho)
        plt.close()

    def evolve(self):
        global geracao
        tempo_inicial = time.process_time()
        self.create_initial_population()
        self.frente = []
        
        self.melhor_individuo = self.populacao[0]
        for i in range(len(self.populacao)):
            if self.populacao[i] < self.melhor_individuo:
                self.melhor_individuo = self.populacao[i]

        self.non_dominated_pareto_sort()
        self.calcula_dados()
        self.plot_frente_de_pareto(str(geracao))
        while time.process_time() - tempo_inicial< 100000:
            print('----', geracao, '----',time.process_time() - tempo_inicial,'s')
            self.crossover()
            self.non_dominated_pareto_sort()
            self.calcula_dados()
            self.mutate()
            self.non_dominated_pareto_sort()
            self.crowding()
            print('fim Crowding')
            self.selection()
            for i in range(len(self.frente)):
                if self.frente[i] < self.melhor_individuo:
                    self.melhor_individuo = self.frente[i]

            print('melhor custo de transporte', self.melhor_individuo.of[0])
            print('melhor emissão de transporte', self.melhor_individuo.of[1])
            print('custo médio',self.custo_medio)
            print('soma média de caminhos',self.emissao_media)
            print('rank médio',self.rank_medio)
            print('melhor rank',self.melhor_rank)
            for i in range(len(grande_frente_pareto)):
                print('(',grande_frente_pareto[i].of[0],'|',grande_frente_pareto[i].of[1],')',end=',')
            print('')
            print('-----------------')
            self.calcula_dados()
            geracao+=1
                
            if len(grande_frente_pareto) > 1:
                self.plot_frente_de_pareto(str(geracao))
        # self.__plot_frente_de_pareto(str(geracao))
    
    
otm = Evolution()
result_omtz = otm.evolve()