import gurobipy as gp
import numpy as np
import math
import random

with open("instances.txt") as file:
    lines = [linha.strip() for linha in file.readlines()]

# Custo do transporte rodoviário
cr = float(lines[0])

# Custo do transporte ferroviário
cf = float(lines[1])

# Custo da multimodalidade
ci = float(lines[2])

# Emissão do transporte rodoviário
er = float(lines[3])

# Emissão do transporte ferroviário
ef = float(lines[4])

# Conjunto de armazéns produtores (N)
N = list(range(1, int(lines[5]) + 1))

# Conjunto de pontos ferroviários (K)
K = list(range(len(N) + 1, len(N) + int(lines[6]) + 1))

# Conjunto de portos de navios destinos (M)
M = list(range(len(N + K) + 1, len(N + K) + int(lines[7]) + 1))

# Conjunto de clientes (O)
O = list(range(1, int(lines[8]) + 1))

# Demanda de cada cliente (em toneladas)
demanda = {}
line_split = lines[9].split(" ")
for o in O:
    demanda[o] = int(line_split[o - 1])

# Oferta de cada armazém produtor (em toneladas)
oferta = {}
line_split = lines[10].split(" ")
for i in N:
    oferta[i] = int(line_split[i - 1])

# Capacidade máxima do porto ferroviário (CF(k))
CF = {}
line_split = lines[11].split(" ")
for k in range(0, len(K)):
    CF[K[k]] = int(line_split[k - 1])
    
# Capacidade máxima do porto de navio (CP(j))
CP = {}
line_split = lines[12].split(" ")
for j in range(0, len(M)):
    CP[M[j]] = int(line_split[j - 1])

pontos = []
for x in range(13, len(lines)):
    line_split = lines[x].split(" ")
    pontos.append([float(line_split[1]), (float(line_split[2]))])
    

# Distância em km entre cada par de locais (armazéns, portos e clientes)
D = {}
def prepare_data():
    # nodes  = []
    # with open('HAHA.txt') as file:
    #     for line in file:
    #         nodes.append(line.split())
    for i in range(len(pontos)):
        for j in range(len(pontos)):
            if i != j:
                D[i + 1, j + 1] = euclidean_distance(int(pontos[i][0]), int(pontos[i][1]), int(pontos[j][0]), int(pontos[j][1]))
                

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
print("HAHHAHAHAHAHAHAH\n")
for k in K:
    for j in M:
        for o in O:
            X[k, j, o] = m.addVar(vtype=gp.GRB.BINARY, lb=0, name="X_{}_{}_{}".format(k, j, o))
print("HAHHAHAHAHAHAHAH\n")
for i in N:
    for j in M:
        for o in O:
            X[i, j, o] = m.addVar(vtype=gp.GRB.BINARY, lb=0, name="X_{}_{}_{}".format(i, j, o))
print("HAHHAHAHAHAHAHAH\n")

y1 = m.addVar(vtype=gp.GRB.BINARY, name="y1")
y2 = m.addVar(vtype=gp.GRB.BINARY, name="y2")

print("HAHHAHAHAHAHAHAH\n")
# Definição da função objetivo
# Função objetivo de custo do transporte
f1 = gp.quicksum(cr * D[i, k] * demanda[o] * X[i, k, o] for i in N for k in K for o in O) + \
     gp.quicksum(cf * D[k, j] * demanda[o] * X[k, j, o] for k in K for j in M for o in O) + \
     gp.quicksum(ci * demanda[o] * X[k, j, o] for k in K for j in M for o in O) + \
     gp.quicksum(cr * D[i, j] * demanda[o] * X[i, j, o] for i in N for j in M for o in O)
       
print("HAHHAHAHAHAHAHAH\n") 
# Função objetivo de minimi0zação de emissão de CO2
f2 = gp.quicksum(er * D[i, k] * demanda[o] * X[i, k, o] for i in N for k in K for o in O) + \
     gp.quicksum(ef * D[k, j] * demanda[o] * X[k, j, o] for j in M for k in K for o in O) + \
     gp.quicksum(er * D[i, j] * demanda[o] * X[i, j, o] for i in N for j in M for o in O)

# m.setObjective(f1, gp.GRB.MINIMIZE)
m.setObjectiveN(f1, 0, priority=2, name="Custo do transporte")
m.setObjectiveN(f2, 1, priority=1, name="Emissão do transporte")

# Oferta dos produtores:
for i in N:
    m.addConstr(gp.quicksum(X[i, k, o] * demanda[o] for k in K for o in O) <= oferta[i] * y1, "Oferta_Prod_{}".format(i))

for i in N:
    m.addConstr(gp.quicksum(X[i, j, o] * demanda[o] for j in M for o in O) <= oferta[i] * y2, "Oferta_Prod_{}".format(i))

# Capacidade dos pontos ferroviários
for k in K:
    m.addConstr(gp.quicksum(X[i, k, o] * demanda[o] for i in N for o in O) <= CF[k] * y1, "Cap_Ferro_{}".format(k))

# Capacidade dos portos de navio
for j in M:
    m.addConstr(gp.quicksum(X[k, j, o] * demanda[o] for k in K for o in O) <= CP[j] * y1, "Cap_Porto_{}".format(j))

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