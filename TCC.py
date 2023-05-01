import gurobipy as gp
import numpy as np
import math
from random import SystemRandom
import pandas as pd
from utils import gen_points

orig = int(input("Quantidade origens: "))
trans = int(input("Quantidade transbordos: "))
port = int(input("Quantidade portos: "))
cli = int(input("Quantidade clientes: "))

points_orig = gen_points.get_point(lim_x_left=-100, lim_x_right=100,
                                   lim_y_down=-100, lim_y_up=100, n=orig)
points_transbordo = gen_points.get_point(lim_x_left=-250, lim_x_right=250,
                                         lim_y_down=-250, lim_y_up=250, n=trans)
points_porto = gen_points.get_point(lim_x_left=-1000, lim_x_right=1000,
                                    lim_y_down=-1000, lim_y_up=1000, n=port)

cost_orig_porto = gen_points.get_cost(points_orig=points_orig, n=orig,
                                      points_dest=points_porto, m=port, tku=1)
cost_orig_trans = gen_points.get_cost(points_orig=points_orig, n=orig,
                                      points_dest=points_transbordo, m=trans, tku=1)
cost_transbordo_porto = gen_points.get_cost(points_orig=points_transbordo, n=trans,
                                            points_dest=points_porto, m=port, tku=1)

# Custo do transporte rodoviário
cr = 0.16

# Custo do transporte ferroviário
cf = 0.08

# Custo da multimodalidade
ci = 0.02

# Emissão do transporte rodoviário
er = 0.2

# Emissão do transporte ferroviário
ef = 0.04

# Conjunto de armazéns produtores (N)
N = list(range(0, orig))

# Conjunto de pontos ferroviários (K)
K = list(range(0, trans))

# Conjunto de portos de navios destinos (M)
M = list(range(0, port))

# Conjunto de clientes (O)
O = list(range(0, cli))

# Demanda de cada cliente (em toneladas)
demmand = [SystemRandom().randint(1, 10000) for _ in range(cli)]

# Oferta de cada armazém produtor (em toneladas)
supply = [sum(demmand) if SystemRandom().random() <= 0.3 else SystemRandom().randint(100, 100000) for _ in range(orig)]

# Capacidade máxima do porto ferroviário (CF(k))
CF = [sum(demmand) if SystemRandom().random() <= 0.3 else SystemRandom().randint(500, 5000) for _ in K]

# Capacidade máxima do porto de navio (CP(j))
CP =[sum(demmand) if SystemRandom().random() <= 0.3 else SystemRandom().randint(1000, 5000) for _ in M]

# breakpoint()
# Criação do modelo
m = gp.Model("Transporte com Transbordo")

# Definição das variáveis de decisão
X = {}
for i in N:
    for k in K:
        for o in O:
            X[i, k, o] = m.addVar(vtype=gp.GRB.BINARY, lb=0, name="X_Produtor_Transbordo_{}_{}_{}".format(i,k,o))
for k in K:
    for j in M:
        for o in O:
            X[k, j, o] = m.addVar(vtype=gp.GRB.BINARY, lb=0, name="X_Transbordo_Porto_{}_{}_{}".format(k, j, o))
for i in N:
    for j in M:
        for o in O:
            X[i, j, o] = m.addVar(vtype=gp.GRB.BINARY, lb=0, name="X_Produtor_Porto{}_{}_{}".format(i, j, o))

y1 = m.addVar(vtype=gp.GRB.BINARY, name="y1")
y2 = m.addVar(vtype=gp.GRB.BINARY, name="y2")

# Definição da função objetivo
# Função objetivo de custo do transporte
f1 = gp.quicksum(cr * cost_orig_trans[i][k] * demmand[o] * X[i, k, o] for i in N for k in K for o in O) + \
     gp.quicksum(cf * cost_transbordo_porto[k][j] * demmand[o] * X[k, j, o] for k in K for j in M for o in O) + \
     gp.quicksum(ci * demmand[o] * X[k, j, o] for k in K for j in M for o in O) + \
     gp.quicksum(cr * cost_orig_porto[i][j] * demmand[o] * X[i, j, o] for i in N for j in M for o in O)
   
# Função objetivo de minimização de emissão de CO2
f2 = gp.quicksum(er * cost_orig_trans[i][k] * demmand[o] * X[i, k, o] for i in N for k in K for o in O) + \
     gp.quicksum(ef * cost_transbordo_porto[k][j] * demmand[o] * X[k, j, o] for j in M for k in K for o in O) + \
     gp.quicksum(er * cost_orig_porto[i][j] * demmand[o] * X[i, j, o] for i in N for j in M for o in O)

# m.setObjective(f1, gp.GRB.MINIMIZE)
m.setObjectiveN(f1, 0, priority=2, name="Custo do transporte")
m.setObjectiveN(f2, 1, priority=1, name="Emissão do transporte")

# Oferta dos produtores:
for i in N:
    m.addConstr(gp.quicksum(X[i, k, o] * demmand[o] for k in K for o in O) <= supply[i] * y1, "Oferta_Prod_{}".format(i))

for i in N:
    m.addConstr(gp.quicksum(X[i, j, o] * demmand[o] for j in M for o in O) <= supply[i] * y2, "Oferta_Prod_{}".format(i))

# Capacidade dos pontos ferroviários
for k in K:
    m.addConstr(gp.quicksum(X[i, k, o] * demmand[o] for i in N for o in O) <= CF[k] * y1, "Cap_Ferro_{}".format(k))

# Capacidade dos portos de navio
for j in M:
    m.addConstr(gp.quicksum(X[k, j, o] * demmand[o] for k in K for o in O) <= CP[j] * y1, "Cap_Porto_{}".format(j))

for o in O:
    m.addConstr(gp.quicksum(X[i, k, o] for i in N for k in K) == 1 * y1)
                    
for o in O:
    m.addConstr(gp.quicksum(X[k, j, o] for k in K for j in M) == 1 * y1)

for o in O:
    m.addConstr(gp.quicksum(X[i, j, o] for i in N for j in M) == 1 * y2)

# Restrição que exige que escolha seja 0 ou 1
m.addConstr(y1 + y2 == 1, "escolha")
# Atualização do modelo com novas variáveis
m.update()
# Otimização do modelo
m.optimize()

m.write("out.sol")