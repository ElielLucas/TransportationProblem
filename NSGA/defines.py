import numpy as np
from utils import gen_points
import random
# N = [0, 1, 2]
# K = [3, 4]
# M = [5, 6, 7]
# demandas_clientes = [100]

# cr = 0.8
# cf = 0.3

# range_trans = len(N)
# range_port = len(N) + len(K)
# range_client = len(N) + len(K) + len(M)

# ofertas = [2000, 2000, 2000]
# capacidade_ferrovias = [3000, 3000]
# capacidade_portos = [3000, 3000, 3000]

# dist_matrix = np.array([
#     [999, 4, 5, 8, 7, 1, 1, 3],
#     [4, 999, 20, 4, 3, 2, 6, 9],
#     [5, 20, 999, 2, 5, 9, 6, 8],
#     [8, 4, 2, 999, 1, 7, 4, 3],
#     [7, 3, 5, 1, 999, 3, 4, 3],
#     [1, 2, 9, 7, 3, 999, 7, 4],
#     [1, 6, 6, 4, 4, 7, 999, 1],
#     [3, 9, 8, 3, 3, 4, 1, 999]    
# ])
er = 0.8
ef = 0.2

with open('input_transport_problem.txt', 'r') as arquivo:
    linhas = arquivo.readlines()
    cr = float(linhas[0].rstrip('\n'))
    cf = float(linhas[1].rstrip('\n'))
    N = linhas[2].split()
    N = [int(valor) for valor in N if valor != '\n']
    K = linhas[3].split()
    K = [int(valor) for valor in K if valor != '\n']
    M = linhas[4].split()
    M = [int(valor) for valor in M if valor != '\n']
    
    demandas = linhas[5].split()
    demandas = [int(valor) for valor in demandas if valor != '\n']
    demandas_clientes = [sum(demandas)]
    
    ofertas = linhas[6].split()
    ofertas = [int(valor) for valor in ofertas if valor != '\n']
    
    capacidade_ferrovias = linhas[7].split()
    capacidade_ferrovias = [int(valor) for valor in capacidade_ferrovias if valor != '\n']
    
    capacidade_portos = linhas[8].split()
    capacidade_portos = [int(valor) for valor in capacidade_portos if valor != '\n']

    points_orig = []
    points_trans = []
    points_portos = []

    for it, i in enumerate(range(9, len(linhas))):
        if it in N:
            pontos = linhas[i].split()
            pontos = [int(valor) for valor in pontos if valor != '\n']
            points_orig.append(pontos)
        elif it in K:
            pontos = linhas[i].split()
            pontos = [int(valor) for valor in pontos if valor != '\n']
            points_trans.append(pontos)
        else:
            pontos = linhas[i].split()
            pontos = [int(valor) for valor in pontos if valor != '\n']
            points_portos.append(pontos)

range_trans = len(N)
range_port = len(N) + len(K)

quantidade_nodes = len(N) + len(K) + len(M)
tempo_matrix = np.full((quantidade_nodes, quantidade_nodes), np.inf)

with open('input_tempo.txt', 'r') as arquivo:
    linhas = arquivo.readlines()
    aux = 0
    for it, i in enumerate(range(0, len(linhas))):
        if it in N:
            pontos = linhas[i].split()
            for it2, tempo in enumerate(pontos):
                tempo_matrix[it][K[it2]] = tempo
        elif it in K:
            pontos = linhas[i].split()
            for it2, tempo in enumerate(pontos):
                tempo_matrix[it][M[it2]] = tempo
        else:
            pontos = linhas[i].split()
            for it2, tempo in enumerate(pontos):
                tempo_matrix[aux][M[it2]] = tempo
            aux += 1
    
dist_matrix = np.full((quantidade_nodes, quantidade_nodes), np.inf)
for i in N:
    for k in K:
        distancia = gen_points.distance(points_orig[i][0], points_orig[i][1], points_trans[k - range_trans][0], points_trans[k - range_trans][1])
        dist_matrix[i, k] = dist_matrix[k, i] = distancia
    
    for m in M:
        distancia = gen_points.distance(points_orig[i][0], points_orig[i][1], points_portos[m - range_port][0], points_portos[m - range_port][1])
        dist_matrix[i, m] = dist_matrix[m, i] = distancia

for k in K:
    for m in M:
        distancia = gen_points.distance(points_trans[k - range_trans][0], points_trans[k - range_trans][1], points_portos[m - range_port][0], points_portos[m - range_port][1])
        dist_matrix[k, m] = dist_matrix[m, k] = distancia
