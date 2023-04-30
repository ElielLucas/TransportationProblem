import gurobipy as gp
import numpy as np
import math
import random

# Conjunto de armazéns produtores (N)
N = [1, 2, 3]

# Conjunto de portos de navios destinos (M)
M = [6, 7, 8, 9]

# Conjunto de pontos ferroviários (K)
K = [4, 5]

# Conjunto de clientes (O)
O = [10]

# Capacidade máxima do porto ferroviário (CF(k))
CF = {4: 80, 5: 3000}

# Capacidade máxima do porto de navio (CP(j))
CP = {6: 50, 7: 9000, 8: 9000, 9: 9000}

# Custo do transporte rodoviário
cr = 0.50

# Custo do transporte ferroviário
cf = 0.25

# Custo da multimodalidade
ci = 0.2

# Emissão do transporte rodoviário
er = 0.6

# Emissão do transporte ferroviário
ef = 0.1

# Oferta de cada armazém produtor (em toneladas)
a = {1: 9000, 2: 500, 3: 700}

# Demanda de cada cliente (em toneladas)
b = {10: 100}

# Distância em km entre cada par de locais (armazéns, portos e clientes)
D = {}

def prepare_data():
    nodes  = []
    with open('HAHA.txt') as file:
        for line in file:
            nodes.append(line.split())
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                D[i + 1, j + 1] = euclidean_distance(int(nodes[i][1]), int(nodes[i][2]), int(nodes[j][1]), int(nodes[j][2]))


def euclidean_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

prepare_data()

# Criação do modelo
m = gp.Model("Transporte com Transbordo")

# Definição das variáveis de decisão
X = {}

for i in N:
    for k in K:
        for o in O:
            X[i, k, o] = m.addVar(vtype=gp.GRB.BINARY, lb=0, name="X_{}_{}_{}".format(i,k,o))
for k in K:
    for j in M:
        for o in O:
            X[k, j, o] = m.addVar(vtype=gp.GRB.BINARY, lb=0, name="X_{}_{}_{}".format(k, j, o))
for i in N:
    for j in M:
        for o in O:
            X[i, j, o] = m.addVar(vtype=gp.GRB.BINARY, lb=0, name="X_{}_{}_{}".format(i, j, o))

y1 = m.addVar(vtype=gp.GRB.BINARY, name="y1")
y2 = m.addVar(vtype=gp.GRB.BINARY, name="y2")

# Definição da função objetivo
# Função objetivo de custo do transporte
f1 = gp.quicksum(cr * D[i, k] * b[o] * X[i, k, o] for i in N for k in K for o in O) + \
     gp.quicksum(cf * D[k, j] * b[o] * X[k, j, o] for k in K for j in M for o in O) + \
     gp.quicksum(ci * b[o] * X[k, j, o] for k in K for j in M for o in O) + \
     gp.quicksum(cr * D[i, j] * b[o] * X[i, j, o] for i in N for j in M for o in O)
       
# Função objetivo de minimização de emissão de CO2
f2 = gp.quicksum(er * D[i, k] * b[o] * X[i, k, o] for i in N for k in K for o in O) + \
     gp.quicksum(ef * D[k, j] * b[o] * X[k, j, o] for j in M for k in K for o in O) + \
     gp.quicksum(er * D[i, j] * b[o] * X[i, j, o] for i in N for j in M for o in O)

# m.setObjective(f1, gp.GRB.MINIMIZE)
m.setObjectiveN(f1, 0, priority=2, name="Custo do transporte")
m.setObjectiveN(f2, 1, priority=1, name="Emissão do transporte")

# Oferta dos produtores:
for i in N:
    m.addConstr(gp.quicksum(X[i, k, o] * b[o] for k in K for o in O) <= a[i] * y1, "Oferta_Prod_{}".format(i))

for i in N:
    m.addConstr(gp.quicksum(X[i, j, o] * b[o] for j in M for o in O) <= a[i] * y2, "Oferta_Prod_{}".format(i))

# Capacidade dos pontos ferroviários
for k in K:
    m.addConstr(gp.quicksum(X[i, k, o] * b[o] for i in N for o in O) <= CF[k] * y1, "Cap_Ferro_{}".format(k))

# Capacidade dos portos de navio
for j in M:
    m.addConstr(gp.quicksum(X[k, j, o] * b[o] for k in K for o in O) <= CP[j] * y1, "Cap_Porto_{}".format(j))

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

breakpoint()