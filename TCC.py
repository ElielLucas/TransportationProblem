import gurobipy as gp
import numpy as np
import math
import random
from utils import gen_points

orig = int(input("Quantidade origens: "))
trans = int(input("Quantidade transbordos: "))
port = int(input("Quantidade portos: "))
cli = int(input("Quantidade clientes: "))

# Custo do transporte rodoviário
cr = 0.7

# Custo do transporte ferroviário
cf = 0.3

# Custo da multimodalidade
ci = 0.04

# Emissão do transporte rodoviário
er = 0.8

# Emissão do transporte ferroviário
ef = 0.2

# Conjunto de armazéns produtores (N)
N = list(range(0, orig))

# Conjunto de pontos ferroviários (K)
K = [(i + orig) for i in range(trans)]

# Conjunto de portos de navios destinos (M)
M = [(i + orig + trans) for i in range(port)]

# Conjunto de clientes (O)
O = [(i + orig + trans + port) for i in range(cli)]

demanda = {}
for o in O:
    demanda[o] = 100

oferta = {}
for i in N:
    oferta[i] = sum(demanda.values()) if random.random() <= 0.3 else random.randint(100, 100000)
    
CF = {}
for k in K:
    CF[k] = sum(demanda.values()) if random.random() <= 0.3 else random.randint(500, 5000)

CP = {}
for j in M:
    CP[j] = sum(demanda.values()) if random.random() <= 0.3 else random.randint(1000, 5000)

points_orig = gen_points.get_point(lim_x_left=-100, lim_x_right=100,
                                   lim_y_down=-100, lim_y_up=100, n=orig)
points_trans = gen_points.get_point(lim_x_left=-250, lim_x_right=250,
                                    lim_y_down=-250, lim_y_up=250, n=trans)
points_portos = gen_points.get_point(lim_x_left=-1000, lim_x_right=1000,
                                     lim_y_down=-1000, lim_y_up=1000, n=port)

# print("Pontos de origem")
# points_orig = []
# for _ in N:
#     points = input("Ponto X e Y: ").split(" ")
#     points_orig.append(gen_points.Point(int(points[0]), int(points[1])))
    
# print("Pontos de transbordo")
# points_trans = []
# for _ in K:
#     points = input("Ponto X e Y: ").split(" ")
#     points_trans.append(gen_points.Point(int(points[0]), int(points[1])))
    
# print("Pontos de porto")
# points_portos = []
# for _ in M:
#     points = input("Ponto X e Y: ").split(" ")
#     points_portos.append(gen_points.Point(int(points[0]), int(points[1])))

dist_orig_trans = {}
for i in N:
    for k in K:
        dist_orig_trans[i, k] = gen_points.distance(points_orig[i].x, points_orig[i].y, points_trans[k - orig].x, points_trans[k - orig].y)

dist_trans_porto = {}
for k in K:
    for j in M:
        dist_trans_porto[k, j] = gen_points.distance(points_trans[k - orig].x, points_trans[k - orig].y, points_portos[j - orig - trans].x, points_portos[j - orig - trans].y)
        
dist_orig_porto = {}
for i in N:
    for j in M:
        dist_orig_porto[i, j] = gen_points.distance(points_orig[i].x, points_orig[i].y, points_portos[j - orig - trans].x, points_portos[j - orig - trans].y)

# Criação do modelo
m = gp.Model("Transporte com Transbordo")

# Definição das variáveis de decisão
X = {}
for i in N:
    for k in K:
        for o in O:
            X[i, k, o] = m.addVar(vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Prod{}_Trans{}_Cliente{}".format(i,k,o))
for k in K:
    for j in M:
        for o in O:
            X[k, j, o] = m.addVar(vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Trans{}_Porto{}_Cliente{}".format(k, j, o))
for i in N:
    for j in M:
        for o in O:
            X[i, j, o] = m.addVar(vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Prod{}_Porto{}_Cliente{}".format(i, j, o))

# Definição da função objetivo
# Função objetivo de custo do transporte
f1 = gp.quicksum(cr * dist_orig_trans[i, k] * X[i, k, o] for i in N for k in K for o in O) + \
     gp.quicksum(cf * dist_trans_porto[k, j] * X[k, j, o] for k in K for j in M for o in O) + \
     gp.quicksum(cr * dist_orig_porto[i, j] * X[i, j, o] for i in N for j in M for o in O)
         

# Função objetivo de minimização de emissão de CO2
f2 = gp.quicksum(er * dist_orig_trans[i, k] * X[i, k, o] for i in N for k in K for o in O) + \
     gp.quicksum(ef * dist_trans_porto[k, j] * X[k, j, o] for j in M for k in K for o in O) + \
     gp.quicksum(er * dist_orig_porto[i, j] * X[i, j, o] for i in N for j in M for o in O)

# m.setObjective(f1, gp.GRB.MINIMIZE)

m.setObjectiveN(f1, 0, priority=2, name="Custo do transporte")
m.setObjectiveN(f2, 1, priority=1, name="Emissão do transporte")

# Oferta dos produtores:
for i in N:
    m.addConstr(((gp.quicksum(X[i, k, o] for k in K for o in O)) + (gp.quicksum(X[i, j, o] for j in M for o in O))) <= oferta[i], "Oferta_Prod_{}".format(i))
    
# Demanda dos clientes:
for o in O:
    m.addConstr(((gp.quicksum(X[i, j, o] for i in N for j in M)) + (gp.quicksum(X[k, j, o] for k in K for j in M))) == demanda[o], "Demanda_Cli_{}".format(o))

# Capacidade dos pontos ferroviários
for k in K:
    m.addConstr(gp.quicksum(X[i, k, o] for i in N for o in O) <= CF[k], "Cap_Ferro_{}".format(k))

# Capacidade dos portos de navio
for j in M:
    m.addConstr(((gp.quicksum(X[i, j, o] for i in N for o in O)) + (gp.quicksum(X[k, j, o] for k in K for o in O))) <= CP[j], "Cap_Porto_{}".format(j))

# Igualdade das quantidades
for k in K:
    m.addConstr((gp.quicksum(X[i, k, o] for i in N for o in O))  == gp.quicksum(X[k, j, o] for j in M for o in O), "Igualdade_{}".format(k))


# Atualização do modelo com novas variáveis
m.update()

# Otimização do modelo
m.optimize()

m.write("out.sol")
