import gurobipy as gp
import numpy as np
import math
import random
import time
from utils import gen_points

orig = int(input("Quantidade origens: "))
trans = int(input("Quantidade transbordos: "))
port = int(input("Quantidade portos: "))
cli = int(input("Quantidade clientes: "))

range_trans = orig
range_port = orig + trans
range_client = orig + trans + port

# Custo do transporte                       
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
K = [(i + range_trans) for i in range(trans)]

# Conjunto de portos de navios destinos (M)
M = [(i + range_port) for i in range(port)]

# Conjunto de clientes (O)
O = [(i + range_client) for i in range(cli)]

demandas = np.random.randint(1, 5000, len(O))

ofertas = np.where(np.random.random(len(N)) <= 0.3, np.sum(demandas), np.random.randint(100, 100000, len(N)))

CF = np.where(np.random.random(len(K)) <= 0.3, np.sum(demandas), np.random.randint(500, 100000, len(K)))

CP = np.where(np.random.random(len(M)) <= 0.3, np.sum(demandas), np.random.randint(1000, 5000, len(M)))

points_orig = gen_points.get_point(lim_x_left=-100, lim_x_right=100,
                                   lim_y_down=-100, lim_y_up=100, n=orig)
points_trans = gen_points.get_point(lim_x_left=-250, lim_x_right=250,
                                    lim_y_down=-250, lim_y_up=250, n=trans)
points_portos = gen_points.get_point(lim_x_left=-1000, lim_x_right=1000,
                                     lim_y_down=-1000, lim_y_up=1000, n=port)

texto = str(cr) + '\n' + str(cf) + '\n'
for i in N:
    texto += str(i) + ' '
texto+='\n'

for i in K:
    texto += str(i) + ' '
texto += '\n'

for i in M:
    texto += str(i) + ' '
texto += '\n'

for i in demandas:
    texto += str(i) + ' '
texto += '\n'

for i in ofertas:
    texto += str(i) + ' '
texto += '\n'

for i in CF:
    texto += str(i) + ' '
texto += '\n'

for i in CP:
    texto += str(i) + ' '
texto += '\n'

for i in points_orig:
    texto += str(i.x) + ' ' + str(i.y) + '\n'
    
for i in points_trans:
    texto += str(i.x) + ' ' + str(i.y) + '\n'
    
for i in points_portos:
    texto += str(i.x) + ' ' + str(i.y) + '\n'


with open('input_transport_problem.txt', 'w') as arquivo:
    arquivo.write(str(texto))

    
dist_orig_trans = {}
for i in N:
    for k in K:
        dist_orig_trans[i, k] = gen_points.distance(points_orig[i].x, points_orig[i].y, points_trans[k - orig].x, points_trans[k - orig].y)

dist_trans_porto = {}
for k in K:
    for j in M:
        dist_trans_porto[k, j] = gen_points.distance(points_trans[k - orig].x, points_trans[k - orig].y, points_portos[j - range_port].x, points_portos[j - range_port].y)
        
dist_orig_porto = {}
for i in N:
    for j in M:
        dist_orig_porto[i, j] = gen_points.distance(points_orig[i].x, points_orig[i].y, points_portos[j - range_port].x, points_portos[j - range_port].y)

start_time = time.time()
# Criação do modelo
m = gp.Model("Transporte com Transbordo")

# # Definição das variáveis de decisão
X = m.addVars(N, K, O, vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Prod_Trans_Cliente")
X.update(m.addVars(K, M, O, vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Trans_Porto_Cliente"))
X.update(m.addVars(N, M, O, vtype=gp.GRB.CONTINUOUS, lb=0, name="X_Prod_Porto_Cliente"))

# Definição da função objetivo
# Função objetivo de custo do transporte
f1 = sum(cr * dist_orig_trans[i, k] * X[i, k, o] for i in N for k in K for o in O)
f1 += sum(cf * dist_trans_porto[k, j] * X[k, j, o] for k in K for j in M for o in O)
f1 += sum(cr * dist_orig_porto[i, j] * X[i, j, o] for i in N for j in M for o in O)
         
# Função objetivo de minimização de emissão de CO2
# f2 = sum(er * dist_orig_trans[i, k] * X[i, k, o] for i in N for k in K for o in O)
# f2 += sum(ef * dist_trans_porto[k, j] * X[k, j, o] for k in K for j in M for o in O)
# f2 += sum(er * dist_orig_porto[i, j] * X[i, j, o] for i in N for j in M for o in O)

m.setObjective(f1, gp.GRB.MINIMIZE)

# m.setObjectiveN(f1, 0, priority=2, name="Custo do transporte")
# m.setObjectiveN(f2, 1, priority=1, name="Emissão do transporte")

# Oferta dos produtores:
for i in N:
    expr = sum([X[i, k, o] for k in K for o in O])
    expr += sum([X[i, j, o] for j in M for o in O])
    m.addConstr(expr <= ofertas[i], "Oferta_Prod_{}".format(i))
    
# Demanda dos clientes:
for o in O:
    expr = sum([X[i, j, o] for i in N for j in M])
    expr += sum([X[k, j, o] for k in K for j in M])
    m.addConstr(expr == demandas[o - range_client], "Demanda_Cli_{}".format(o))

# Capacidade dos pontos ferroviários
for k in K:
    expr = sum([X[i, k, o] for i in N for o in O])
    m.addConstr(expr <= CF[k - range_trans], "Cap_Ferro_{}".format(k))

# Capacidade dos portos de navio
for j in M: 
    expr = sum([X[i, j, o] for i in N for o in O])
    expr += sum([X[k, j, o] for k in K for o in O])
    m.addConstr(expr <= CP[j - range_port], "Cap_Porto_{}".format(j))

# Igualdade das quantidades
for k in K:
    expr1 = sum([X[i, k, o] for i in N for o in O])
    expr2 = sum([X[k, j, o] for j in M for o in O])
    m.addConstr(expr1 == expr2), "Igualdade_{}".format(k)


# Atualização do modelo com novas variáveis
m.update()

m.setParam('TimeLimit', 60*9)
m.setParam(gp.GRB.Param.Threads, 1)
# m.setParam('NodefileStart', nodefile)

# Otimização do modelo
m.optimize()

total_time = time.time() - start_time
print("Total time: ", total_time)

# Verificar o status da otimização
status = m.status
if status == gp.GRB.OPTIMAL:
    pass
    # A otimização foi bem-sucedida, faça algo com a solução
    # solution = m.getAttr('x', m.getVars())
elif status == gp.GRB.TIME_LIMIT:
    print('Limite de tempo atingido, a solução não foi encontrada dentro do tempo definido.')
else:
    print('A otimização foi interrompida devido a um erro ou outro motivo.')


# m.write("out.sol")    
