import gurobipy as gp
import numpy as np
import math
import random
import time
import input as inp
from utils import gen_points

class Gurobi:
    def __init__(self):
        self.criar_instancia()
        
        # Criação do modelo
        self.m = gp.Model("Transporte com Transbordo")

        # Definição das variáveis de decisão
        X = self.m.addVars(self.N, self.K, self.O, vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Prod_Trans_Cliente")
        X.update(self.m.addVars(self.K, self.M, self.O, vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Trans_Porto_Cliente"))
        X.update(self.m.addVars(self.N, self.M, self.O, vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Prod_Porto_Cliente"))

        # Definição da função objetivo
        # Função objetivo de custo do transporte
        self.f1 = sum(self.cr * self.dist_orig_trans[i, k] * X[i, k, o] for i in self.N for k in self.K for o in self.O)
        self.f1 += sum(self.cf * self.dist_trans_porto[k, j] * X[k, j, o] for k in self.K for j in self.M for o in self.O)
        self.f1 += sum(self.cr * self.dist_orig_porto[i, j] * X[i, j, o] for i in self.N for j in self.M for o in self.O)
                
        # Função objetivo de minimização de emissão de CO2
        self.f2 = sum(self.er * inp.tempo_matrix[i, k] * X[i, k, o] for i in self.N for k in self.K for o in self.O)
        self.f2 += sum(self.ef * inp.tempo_matrix[k, j] * X[k, j, o] for k in self.K for j in self.M for o in self.O)
        self.f2 += sum(self.er * inp.tempo_matrix[i, j] * X[i, j, o] for i in self.N for j in self.M for o in self.O)

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

            
            
    def criar_instancia(self):
        # self.orig = random.randint(1, qtd_origens)
        # self.trans = random.randint(1, qtd_trans)
        # self.port = random.randint(1, qtd_port)
        # self.cli = random.randint(1, qtd_cli)

        # Custo do transporte                       
        self.cr = 0.239

        # Custo do transporte ferroviário
        self.cf = 0.067

        # Custo da multimodalidade
        self.ci = 0.04

        # Emissão do transporte rodoviário
        self.er = 52.77 

        # Emissão do transporte ferroviário
        self.ef = 18.05

        # Conjunto de armazéns produtores (N)
        self.N = inp.N

        # Conjunto de pontos ferroviários (K)
        self.K = inp.K

        # Conjunto de portos de navios destinos (M)
        self.M = inp.M

        # Conjunto de clientes (O)
        self.O = inp.O
        
        self.range_trans = len(self.N)
        self.range_port = len(self.N) + len(self.K)
        self.range_client = len(self.N) + len(self.K) + len(self.M)

        self.demandas = inp.demandas

        self.ofertas = inp.ofertas

        self.CF = inp.CF

        self.CP = inp.CP


        quantidade_nodes = len(self.N) + len(self.K) + len(self.M)
        self.tempo_matrix = np.full((quantidade_nodes, quantidade_nodes), np.inf)

        self.dist_orig_trans = inp.dist_orig_trans

        self.dist_trans_porto = inp.dist_trans_porto
                
        self.dist_orig_porto = inp.dist_orig_porto
    
