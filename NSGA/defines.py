import numpy as np

N = [0, 1, 2]
K = [3, 4]
M = [5, 6, 7]
demandas_clientes = [50, 100]

cr = 0.8
cf = 0.3

range_trans = len(N)
range_port = len(N) + len(K)
range_client = len(N) + len(K) + len(M)

ofertas = [2000, 2000, 2000]
capacidade_ferrovias = [3000, 3000]
capacidade_portos = [3000, 3000, 3000]

dist_matrix = np.array([
    [999, 4, 5, 8, 7, 1, 1, 3],
    [4, 999, 20, 4, 3, 2, 6, 9],
    [5, 20, 999, 2, 5, 9, 6, 8],
    [8, 4, 2, 999, 1, 7, 4, 3],
    [7, 3, 5, 1, 999, 3, 4, 3],
    [1, 2, 9, 7, 3, 999, 7, 4],
    [1, 6, 6, 4, 4, 7, 999, 1],
    [3, 9, 8, 3, 3, 4, 1, 999]    
])