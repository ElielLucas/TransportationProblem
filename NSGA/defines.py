import numpy as np

N = [0, 1, 2]
K = [3, 4]
M = [5, 6, 7]
demandas_clientes = [30]

range_trans = len(N)
range_port = len(N) + len(K)
range_client = len(N) + len(K) + len(M)

ofertas = [30, 100, 20]
demandas = [5, 6, 15]
capacidade_ferrovias = [100, 50]
capacidade_portos = [100, 100, 100]

dist_matrix = np.array([
    [999, 4, 5, 8, 7, 1, 1, 3],
    [10, 999, 20, 4, 3, 2, 6, 9],
    [4, 3, 999, 2, 5, 9, 6, 8],
    [1, 6, 3, 999, 1, 7, 4, 3],
    [9, 5, 6, 6, 999, 3, 4, 3],
    [7, 9, 5, 6, 2, 999, 7, 4],
    [2, 9, 6, 2, 7, 9, 999, 1],
    [8, 2, 4, 20, 4, 3, 5, 999]    
])