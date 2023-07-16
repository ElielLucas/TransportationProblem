import random 

N = [0,1,2,3,4]
K = [5,6,7,8]
M = [9,10]
O = [11]
ofertas = [243138, 1253270, 755250, 354063, 143703]
demandas = [2649422]

CF = [1709592, 691205, 125374, 223253]
CP = [172389, 2577035]
quantidade_nodes = len(N) + len(K) + len(M)
import numpy as np

dist_orig_trans = {}
dist_orig_trans[0, 0] = 999999
dist_orig_trans[1, 1] = 999999
dist_orig_trans[2, 2] = 999999
dist_orig_trans[3, 3] = 999999
dist_orig_trans[4, 4] = 999999
dist_orig_trans[0, 1] = 999999
dist_orig_trans[1, 0] = 999999
dist_orig_trans[0, 2] = 999999
dist_orig_trans[2, 0] = 999999
dist_orig_trans[0, 3] = 999999
dist_orig_trans[3, 0] = 999999
dist_orig_trans[0, 4] = 999999
dist_orig_trans[4, 0] = 999999
dist_orig_trans[0, 5] = 372
dist_orig_trans[5, 0] = 372
dist_orig_trans[0, 6] = 408
dist_orig_trans[6, 0] = 408
dist_orig_trans[0, 7] = 523
dist_orig_trans[7, 0] = 523
dist_orig_trans[0, 8] = 588
dist_orig_trans[8, 0] = 588

# random.uniform(20, random.choice([60, 80]))
dist_orig_trans[1, 5] = 392
dist_orig_trans[1, 6] = 256
dist_orig_trans[1, 7] = 367
dist_orig_trans[1, 8] = 62 

dist_orig_trans[2, 5] = 499
dist_orig_trans[2, 6] = 223
dist_orig_trans[2, 7] = 548
dist_orig_trans[2, 8] = 173

dist_orig_trans[3, 5] = 654
dist_orig_trans[3, 6] = 392
dist_orig_trans[3, 7] = 772
dist_orig_trans[3, 8] = 586

dist_orig_trans[4, 5] = 249
dist_orig_trans[4, 6] = 57
dist_orig_trans[4, 7] = 367
dist_orig_trans[4, 8] = 204


dist_trans_porto = {}
dist_trans_porto[5, 9] = 2079
dist_trans_porto[5, 10] = 1213
dist_trans_porto[6, 9] = 2298
dist_trans_porto[6, 10] = 989
dist_trans_porto[7, 9] = 1536
dist_trans_porto[7, 10] = 1034
dist_trans_porto[8, 9] = 1751
dist_trans_porto[8, 10] = 1541

dist_orig_porto = {}
dist_orig_porto[0, 9] = 1753
dist_orig_porto[0, 10] = 1354
dist_orig_porto[1, 9] = 1150
dist_orig_porto[1, 10] = 774
dist_orig_porto[2, 9] = 1136
dist_orig_porto[2, 10] = 957
dist_orig_porto[3, 9] = 1652
dist_orig_porto[3, 10] = 1441
dist_orig_porto[4, 9] = 1418
dist_orig_porto[4, 10] = 1010


tempo_matrix = np.full((quantidade_nodes, quantidade_nodes), np.inf)

for i in N:
    for k in K:
        velocidade_media = random.uniform(30, random.choice([60, 80]))
        tempo = dist_orig_trans[i, k] / velocidade_media
        tempo_matrix[i, k] = tempo
    
    for m in M:
        velocidade_media = random.uniform(30, random.choice([60, 80]))
        tempo = dist_orig_porto[i, m] / velocidade_media
        tempo_matrix[i, m] = tempo

for k in K:
    for m in M:
        velocidade_media = random.uniform(30, 40)
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
dist_matrix[0, 1] = 999999
dist_matrix[1, 0] = 999999
dist_matrix[0, 2] = 999999
dist_matrix[2, 0] = 999999
dist_matrix[0, 3] = 999999
dist_matrix[3, 0] = 999999
dist_matrix[0, 4] = 999999
dist_matrix[4, 0] = 999999
dist_matrix[0, 5] = 372
dist_matrix[5, 0] = 372
dist_matrix[0, 6] = 408
dist_matrix[6, 0] = 408
dist_matrix[0, 7] = 523
dist_matrix[7, 0] = 523
dist_matrix[0, 8] = 588
dist_matrix[8, 0] = 588

# random.uniform(20, random.choice([60, 80]))
dist_matrix[1, 5] = 392
dist_matrix[1, 6] = 256
dist_matrix[1, 7] = 367
dist_matrix[1, 8] = 62

dist_matrix[2, 5] = 499
dist_matrix[2, 6] = 223
dist_matrix[2, 7] = 548
dist_matrix[2, 8] = 173

dist_matrix[3, 5] = 654
dist_matrix[3, 6] = 392
dist_matrix[3, 7] = 772
dist_matrix[3, 8] = 586

dist_matrix[4, 5] = 249
dist_matrix[4, 6] = 57
dist_matrix[4, 7] = 367
dist_matrix[4, 8] = 204

dist_matrix[5, 9] = 2079
dist_matrix[5, 10] = 1213
dist_matrix[6, 9] = 2298
dist_matrix[6, 10] = 989
dist_matrix[7, 9] = 1536
dist_matrix[7, 10] = 1034
dist_matrix[8, 9] = 1751
dist_matrix[8, 10] = 1541

dist_matrix[0, 9] = 1753
dist_matrix[0, 10] = 1354
dist_matrix[1, 9] = 1150
dist_matrix[1, 10] = 774
dist_matrix[2, 9] = 1136
dist_matrix[2, 10] = 957
dist_matrix[3, 9] = 1652
dist_matrix[3, 10] = 1441
dist_matrix[4, 9] = 1418
dist_matrix[4, 10] = 1010


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









# dist_matrix =
# dist_trans_porto = 
# dist_orig_porto =
