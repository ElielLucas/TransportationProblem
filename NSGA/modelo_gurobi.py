import gurobipy as gp
import numpy as np
import math
import random
import time
from utils import gen_points

class Gurobi:
    def __init__(self, nome_instancia, iteracao, qtd_origens, qtd_trans, qtd_portos, qtd_clientes):
        self.criar_instancia(nome_instancia, iteracao, qtd_origens, qtd_trans, qtd_portos, qtd_clientes)
        
        # Criação do modelo
        self.m = gp.Model("Transporte com Transbordo")

        # # Definição das variáveis de decisão
        X = self.m.addVars(self.N, self.K, self.O, vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Prod_Trans_Cliente")
        X.update(self.m.addVars(self.K, self.M, self.O, vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Trans_Porto_Cliente"))
        X.update(self.m.addVars(self.N, self.M, self.O, vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Prod_Porto_Cliente"))

        # Definição da função objetivo
        # Função objetivo de custo do transporte
        self.f1 = sum(self.cr * self.dist_orig_trans[i, k] * X[i, k, o] for i in self.N for k in self.K for o in self.O)
        self.f1 += sum(self.cf * self.dist_trans_porto[k, j] * X[k, j, o] for k in self.K for j in self.M for o in self.O)
        self.f1 += sum(self.cr * self.dist_orig_porto[i, j] * X[i, j, o] for i in self.N for j in self.M for o in self.O)
                
        # Função objetivo de minimização de emissão de CO2
        self.f2 = sum(self.er * self.tempo_matrix[i, k] * X[i, k, o] for i in self.N for k in self.K for o in self.O)
        self.f2 += sum(self.ef * self.tempo_matrix[k, j] * X[k, j, o] for k in self.K for j in self.M for o in self.O)
        self.f2 += sum(self.er * self.tempo_matrix[i, j] * X[i, j, o] for i in self.N for j in self.M for o in self.O)

        # Oferta dos produtores:
        for i in self.N:
            expr = sum([X[i, k, o] for k in self.K for o in self.O])
            expr += sum([X[i, j, o] for j in self.M for o in self.O])
            self.m.addConstr(expr <= self.ofertas[i], "Oferta_Prod_{}".format(i))
            
        # Demanda dos clientes:
        for o in self.O:
            expr = sum([X[i, j, o] for i in self.N for j in self.M])
            expr += sum([X[k, j, o] for k in self.K for j in self.M])
            self.m.addConstr(expr == self.demandas[o - self.range_client], "Demanda_Cli_{}".format(o))

        # Capacidade dos pontos ferroviários
        for k in self.K:
            expr = sum([X[i, k, o] for i in self.N for o in self.O])
            self.m.addConstr(expr <= self.CF[k - self.range_trans], "Cap_Ferro_{}".format(k))

        # Capacidade dos portos de navio
        for j in self.M: 
            expr = sum([X[i, j, o] for i in self.N for o in self.O])
            expr += sum([X[k, j, o] for k in self.K for o in self.O])
            self.m.addConstr(expr <= self.CP[j - self.range_port], "Cap_Porto_{}".format(j))

        # Igualdade das quantidades
        for k in self.K:
            expr1 = sum([X[i, k, o] for i in self.N for o in self.O])
            expr2 = sum([X[k, j, o] for j in self.M for o in self.O])
            self.m.addConstr(expr1 == expr2), "Igualdade_{}".format(k)
        # m.setObjective(f1, gp.GRB.MINIMIZE)
        self.m.setObjectiveN(self.f1, 0, priority=2, name="Custo do transporte")
        self.m.setObjectiveN(self.f2, 1, priority=1, name="Emissão do transporte")
        # Atualização do modelo com novas variáveis

        self.m.setParam('TimeLimit', 60*9)
        self.m.setParam(gp.GRB.Param.Threads, 1)
        
        self.m.update()
        
    def otimizar(self):
        # Otimização do modelo
        self.m.optimize()

        # Verificar o status da otimização
        status = self.m.status
        if status == gp.GRB.OPTIMAL:
            return self.f1.getValue(), self.f2.getValue()
        elif status == gp.GRB.TIME_LIMIT:
            print('Limite de tempo atingido, a solução não foi encontrada dentro do tempo definido.')
            return 0, 0
        else:
            print('A otimização foi interrompida devido a um erro ou outro motivo.')
            return 0, 0

            
            
    def criar_instancia(self, nome_instancia, iteracao, qtd_origens, qtd_trans, qtd_port, qtd_cli):
        self.orig = random.randint(1, qtd_origens)
        self.trans = random.randint(1, qtd_trans)
        self.port = random.randint(1, qtd_port)
        self.cli = random.randint(1, qtd_cli)
        while (self.orig * self.trans * self.port * self.cli > 1000000) and self.trans > self.orig and self.trans > self.port and self.port > self.orig:
            self.orig = random.randint(1, qtd_origens)
            self.trans = random.randint(1, qtd_trans)
            self.port = random.randint(1, qtd_port)
            self.cli = random.randint(1, qtd_cli)

        self.range_trans = self.orig
        self.range_port = self.orig + self.trans
        self.range_client = self.orig + self.trans + self.port

        # Custo do transporte                       
        self.cr = 0.7

        # Custo do transporte ferroviário
        self.cf = 0.3

        # Custo da multimodalidade
        self.ci = 0.04

        # Emissão do transporte rodoviário
        self.er = 0.8

        # Emissão do transporte ferroviário
        self.ef = 0.2

        # Conjunto de armazéns produtores (N)
        self.N = list(range(0, self.orig))

        # Conjunto de pontos ferroviários (K)
        self.K = [(i + self.range_trans) for i in range(self.trans)]

        # Conjunto de portos de navios destinos (M)
        self.M = [(i + self.range_port) for i in range(self.port)]

        # Conjunto de clientes (O)
        self.O = [(i + self.range_client) for i in range(self.cli)]

        self.demandas = np.random.randint(1, 5000, len(self.O))

        self.ofertas = np.where(np.random.random(len(self.N)) <= 0.3, np.sum(self.demandas), np.random.randint(100, 100000, len(self.N)))

        self.CF = np.where(np.random.random(len(self.K)) <= 0.3, np.sum(self.demandas), np.random.randint(500, 100000, len(self.K)))

        self.CP = np.where(np.random.random(len(self.M)) <= 0.3, np.sum(self.demandas), np.random.randint(1000, 5000, len(self.M)))

        points_orig = gen_points.get_point(lim_x_left=-100, lim_x_right=100,
                                           lim_y_down=-100, lim_y_up=100, n=self.orig)
        points_trans = gen_points.get_point(lim_x_left=-250, lim_x_right=250,
                                            lim_y_down=-250, lim_y_up=250, n=self.trans)
        points_portos = gen_points.get_point(lim_x_left=-1000, lim_x_right=1000,
                                            lim_y_down=-1000, lim_y_up=1000, n=self.port)

        texto = str(self.cr) + '\n' + str(self.cf) + '\n'
        for i in self.N:
            texto += str(i) + ' '
        texto+='\n'

        for i in self.K:
            texto += str(i) + ' '
        texto += '\n'

        for i in self.M:
            texto += str(i) + ' '
        texto += '\n'

        for i in self.demandas:
            texto += str(i) + ' '
        texto += '\n'

        for i in self.ofertas:
            texto += str(i) + ' '
        texto += '\n'

        for i in self.CF:
            texto += str(i) + ' '
        texto += '\n'

        for i in self.CP:
            texto += str(i) + ' '
        texto += '\n'

        for i in points_orig:
            texto += str(i.x) + ' ' + str(i.y) + '\n'
            
        for i in points_trans:
            texto += str(i.x) + ' ' + str(i.y) + '\n'
            
        for i in points_portos:
            texto += str(i.x) + ' ' + str(i.y) + '\n'


        quantidade_nodes = len(self.N) + len(self.K) + len(self.M)
        self.tempo_matrix = np.full((quantidade_nodes, quantidade_nodes), np.inf)
        texto_tempo = ''

        self.dist_orig_trans = {}
        for i in self.N:
            for k in self.K:
                self.dist_orig_trans[i, k] = gen_points.distance(points_orig[i].x, points_orig[i].y, points_trans[k - self.orig].x, points_trans[k - self.orig].y)
                velocidade_media = random.uniform(20, random.choice([60, 80]))
                tempo = self.dist_orig_trans[i, k] / velocidade_media
                self.tempo_matrix[i, k] = tempo
                texto_tempo += str(tempo) + ' '
            texto_tempo += '\n'


        self.dist_trans_porto = {}
        for k in self.K:
            for j in self.M:
                self.dist_trans_porto[k, j] = gen_points.distance(points_trans[k - self.orig].x, points_trans[k - self.orig].y, points_portos[j - self.range_port].x, points_portos[j - self.range_port].y)
                tempo = self.tempo_matrix[j, k] = self.dist_trans_porto[k, j] / random.uniform(70, 150)
                self.tempo_matrix[k, j] = tempo
                texto_tempo += str(tempo) + ' '
            texto_tempo += '\n'
                
        self.dist_orig_porto = {}
        for i in self.N:
            for j in self.M:
                self.dist_orig_porto[i, j] = gen_points.distance(points_orig[i].x, points_orig[i].y, points_portos[j - self.range_port].x, points_portos[j - self.range_port].y)
                velocidade_media = random.uniform(20, random.choice([60, 80]))
                tempo = self.dist_orig_porto[i, j] / velocidade_media
                self.tempo_matrix[i, j] = tempo
                texto_tempo += str(tempo) + ' '
            texto_tempo += '\n'


        with open(nome_instancia + str(iteracao) + '.txt', 'w') as arquivo:
            arquivo.write(str(texto))
            
        with open(nome_instancia + str(iteracao) + '_tempo.txt', 'w') as arquivo:
            arquivo.write(str(texto_tempo))
    
