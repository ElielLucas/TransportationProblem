import random 

N = [0,1,2,3,4,5]
K = [6,7,8,9]
M = [10,11]
O = [12]
ofertas = [1500.714, 275.486, 542.768, 383.352, 314.838, 82.057]
demandas = [1200, 200]
demandas = [sum(demandas)]

CF = [2169.451, 743811.6, 61984.3, 123968.6]
CP = [1268.522, 17589.232]
quantidade_nodes = len(N) + len(K) + len(M)
import numpy as np

dist_orig_trans = {}
dist_orig_trans[0, 0] = 999999
dist_orig_trans[1, 1] = 999999
dist_orig_trans[2, 2] = 999999
dist_orig_trans[3, 3] = 999999
dist_orig_trans[4, 4] = 999999
dist_orig_trans[5, 5] = 999999
dist_orig_trans[0, 1] = 999999
dist_orig_trans[1, 0] = 999999
dist_orig_trans[0, 2] = 999999
dist_orig_trans[2, 0] = 999999
dist_orig_trans[0, 3] = 999999
dist_orig_trans[3, 0] = 999999
dist_orig_trans[0, 4] = 999999
dist_orig_trans[4, 0] = 999999
dist_orig_trans[0, 5] = 999999
dist_orig_trans[5, 0] = 999999
dist_orig_trans[0, 6] = 0
dist_orig_trans[6, 0] = 0
dist_orig_trans[0, 7] = 999999
dist_orig_trans[7, 0] = 999999
dist_orig_trans[0, 8] = 999999
dist_orig_trans[8, 0] = 999999
dist_orig_trans[0, 9] = 999999
dist_orig_trans[9, 0] = 999999
dist_orig_trans[0, 10] = 999999
dist_orig_trans[10, 0] = 999999
dist_orig_trans[0, 11] = 999999
dist_orig_trans[11, 0] = 999999

# random.uniform(20, random.choice([60, 80]))
dist_orig_trans[1, 9] = 256
dist_orig_trans[1, 6] = 392
dist_orig_trans[1, 7] = 365
dist_orig_trans[1, 8] = 62
dist_orig_trans[2, 9] = 223
dist_orig_trans[2, 6] = 499
dist_orig_trans[2, 7] = 548
dist_orig_trans[2, 8] = 173
dist_orig_trans[3, 9] = 272
dist_orig_trans[3, 6] = 137
dist_orig_trans[3, 7] = 226
dist_orig_trans[3, 8] = 240
dist_orig_trans[4, 9] = 0
dist_orig_trans[4, 6] = 999999
dist_orig_trans[4, 7] = 999999
dist_orig_trans[4, 8] = 999999
dist_orig_trans[5, 9] = 999999
dist_orig_trans[5, 6] = 999999
dist_orig_trans[5, 7] = 0
dist_orig_trans[5, 8] = 999999

dist_trans_porto = {}
dist_trans_porto[6, 10] = 2079
dist_trans_porto[6, 11] = 1212
dist_trans_porto[7, 10] = 2298
dist_trans_porto[7, 11] = 989
dist_trans_porto[8, 10] = 1751
dist_trans_porto[8, 11] = 1034
dist_trans_porto[9, 10] = 1800
dist_trans_porto[9, 11] = 1541

dist_orig_porto = {}
dist_orig_porto[0, 10] = 1406
dist_orig_porto[0, 11] = 977
dist_orig_porto[1, 10] = 1150
dist_orig_porto[1, 11] = 774
dist_orig_porto[2, 10] = 1136
dist_orig_porto[2, 11] = 957
dist_orig_porto[3, 10] = 1271
dist_orig_porto[3, 11] = 841
dist_orig_porto[4, 10] = 1377
dist_orig_porto[4, 11] = 1040
dist_orig_porto[5, 10] = 1329
dist_orig_porto[5, 11] = 819


tempo_matrix = np.full((quantidade_nodes, quantidade_nodes), np.inf)

for i in N:
    for k in K:
        velocidade_media = random.uniform(40, random.choice([60, 80]))
        tempo = dist_orig_trans[i, k] / velocidade_media
        tempo_matrix[i, k] = tempo
    
    for m in M:
        velocidade_media = random.uniform(40, random.choice([60, 80]))
        tempo = dist_orig_porto[i, m] / velocidade_media
        tempo_matrix[i, m] = tempo

for k in K:
    for m in M:
        velocidade_media = random.uniform(20, 40)
        tempo = dist_trans_porto[k, m] / velocidade_media
        tempo_matrix[k, m] = tempo
                
# tempo_matrix[0, 6] = 0.0
# tempo_matrix[6, 0] = 0.0

# # random.uniform(20, random.choice([60, 80]))
# tempo_matrix[1, 9] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[1, 6] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[1, 7] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[1, 8] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[2, 9] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[2, 6] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[2, 7] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[2, 8] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[3, 9] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[3, 6] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[3, 7] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[3, 8] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[4, 9] = 0
# tempo_matrix[5, 7] = 0

# tempo_matrix[6, 10] = random.uniform(20, 40)
# tempo_matrix[6, 11] = random.uniform(20, 40)
# tempo_matrix[7, 10] = random.uniform(20, 40)
# tempo_matrix[7, 11] = random.uniform(20, 40)
# tempo_matrix[8, 10] = random.uniform(20, 40)
# tempo_matrix[8, 11] = random.uniform(20, 40)
# tempo_matrix[9, 10] = random.uniform(20, 40)
# tempo_matrix[9, 11] = random.uniform(20, 40)

# tempo_matrix[0, 10] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[0, 11] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[1, 10] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[1, 11] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[2, 10] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[2, 11] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[3, 10] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[3, 11] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[4, 10] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[4, 11] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[5, 10] = random.uniform(20, random.choice([60, 80]))
# tempo_matrix[5, 11] = random.uniform(20, random.choice([60, 80]))

dist_matrix = np.full((quantidade_nodes, quantidade_nodes), np.inf)
dist_matrix[0, 0] = 999999
dist_matrix[1, 1] = 999999
dist_matrix[2, 2] = 999999
dist_matrix[3, 3] = 999999
dist_matrix[4, 4] = 999999
dist_matrix[5, 5] = 999999
dist_matrix[0, 1] = 999999
dist_matrix[1, 0] = 999999
dist_matrix[0, 2] = 999999
dist_matrix[2, 0] = 999999
dist_matrix[0, 3] = 999999
dist_matrix[3, 0] = 999999
dist_matrix[0, 4] = 999999
dist_matrix[4, 0] = 999999
dist_matrix[0, 5] = 999999
dist_matrix[5, 0] = 999999
dist_matrix[0, 6] = 0
dist_matrix[6, 0] = 0
dist_matrix[0, 7] = 999999
dist_matrix[7, 0] = 999999
dist_matrix[0, 8] = 999999
dist_matrix[8, 0] = 999999
dist_matrix[0, 9] = 999999
dist_matrix[9, 0] = 999999
dist_matrix[0, 10] = 999999
dist_matrix[10, 0] = 999999
dist_matrix[0, 11] = 999999
dist_matrix[11, 0] = 999999

dist_matrix[1, 9] = 256
dist_matrix[1, 6] = 392
dist_matrix[1, 7] = 365
dist_matrix[1, 8] = 62
dist_matrix[2, 9] = 223
dist_matrix[2, 6] = 499
dist_matrix[2, 7] = 548
dist_matrix[2, 8] = 173
dist_matrix[3, 9] = 272
dist_matrix[3, 6] = 137
dist_matrix[3, 7] = 226
dist_matrix[3, 8] = 240
dist_matrix[4, 9] = 0
dist_matrix[4, 6] = 999999
dist_matrix[4, 7] = 999999
dist_matrix[4, 8] = 999999
dist_matrix[5, 9] = 999999
dist_matrix[5, 6] = 999999
dist_matrix[5, 7] = 0
dist_matrix[5, 8] = 999999

dist_matrix[6, 10] = 2079
dist_matrix[6, 11] = 1213
dist_matrix[7, 10] = 2298
dist_matrix[7, 11] = 989
dist_matrix[8, 10] = 1751
dist_matrix[8, 11] = 1034
dist_matrix[9, 10] = 1800
dist_matrix[9, 11] = 1541

dist_matrix[0, 10] = 1406
dist_matrix[0, 11] = 977
dist_matrix[1, 10] = 1150
dist_matrix[1, 11] = 774
dist_matrix[2, 10] = 1136
dist_matrix[2, 11] = 957
dist_matrix[3, 10] = 1271
dist_matrix[3, 11] = 841
dist_matrix[4, 10] = 1377
dist_matrix[4, 11] = 1040
dist_matrix[5, 10] = 1329
dist_matrix[5, 11] = 819


range_trans = len(N)
range_port = len(N) + len(K)
range_client = len(N) + len(K) + len(M)


cr = 15.42

# Custo do transporte ferroviário
cf = 7.03

# Custo da multimodalidade
ci = 0.04

# Emissão do transporte rodoviário
er = 52.77 

# Emissão do transporte ferroviário
ef = 18.05









# dist_orig_trans =
# dist_trans_porto = 
# dist_orig_porto =
