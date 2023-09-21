import random 
import numpy as np

N = [0,1,2,3,4,5]
K = [6,7,8,9]
M = [10,11,12]
O = [13]
ofertas = [243138, 1253270, 755250, 354063, 143703, 1631300]
demandas = [2240100]
# 4240100
# 223253
CF = [2642735, 1068484, 193806, 345111]
CP = [266483, 3983654, 100000] #Aquiiiii
quantidade_nodes = len(N) + len(K) + len(M)

dist_orig_trans = {}
# De cada origem para ela mesma
dist_orig_trans[0, 0] = 999999
dist_orig_trans[1, 1] = 999999
dist_orig_trans[2, 2] = 999999
dist_orig_trans[3, 3] = 999999
dist_orig_trans[4, 4] = 999999
dist_orig_trans[5, 5] = 999999

# De cada origem para cada uma das outras origens
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

# De Aragarças para cada um dos transbordos
dist_orig_trans[0, 6] = 408
dist_orig_trans[6, 0] = 408
dist_orig_trans[0, 7] = 372
dist_orig_trans[7, 0] = 372
dist_orig_trans[0, 8] = 523
dist_orig_trans[8, 0] = 523
dist_orig_trans[0, 9] = 588
dist_orig_trans[9, 0] = 588

# De Catalão para cada um dos transbordos
dist_orig_trans[1, 6] = 256
dist_orig_trans[6, 1] = 256
dist_orig_trans[1, 7] = 392
dist_orig_trans[7, 1] = 392
dist_orig_trans[1, 8] = 367
dist_orig_trans[8, 1] = 367
dist_orig_trans[1, 9] = 62 
dist_orig_trans[9, 1] = 62 

# De Cristalina para cada um dos transbordos
dist_orig_trans[2, 6] = 223
dist_orig_trans[6, 2] = 223
dist_orig_trans[2, 7] = 499
dist_orig_trans[7, 2] = 499
dist_orig_trans[2, 8] = 550
dist_orig_trans[8, 2] = 550
dist_orig_trans[2, 9] = 173
dist_orig_trans[9, 2] = 173

# De Porangatu para cada um dos transbordos
dist_orig_trans[3, 6] = 392
dist_orig_trans[6, 3] = 392
dist_orig_trans[3, 7] = 654
dist_orig_trans[7, 3] = 654
dist_orig_trans[3, 8] = 772
dist_orig_trans[8, 3] = 772
dist_orig_trans[3, 9] = 586
dist_orig_trans[9, 3] = 586

# De Goiânia para cada um dos transbordos
dist_orig_trans[4, 6] = 57
dist_orig_trans[6, 4] = 57
dist_orig_trans[4, 7] = 249
dist_orig_trans[7, 4] = 249
dist_orig_trans[4, 8] = 367
dist_orig_trans[8, 4] = 367
dist_orig_trans[4, 9] = 204
dist_orig_trans[9, 4] = 204

# AQUIIII
# De Rio Verde para cada um dos transbordos
dist_orig_trans[5, 6] = 691
dist_orig_trans[6, 5] = 691
dist_orig_trans[5, 7] = 977
dist_orig_trans[7, 5] = 977
dist_orig_trans[5, 8] = 1113
dist_orig_trans[8, 5] = 1113
dist_orig_trans[5, 9] = 811
dist_orig_trans[9, 5] = 811


dist_trans_porto = {}
# De Anapolis para todos os portos
dist_trans_porto[6, 10] = 1751
dist_trans_porto[10, 6] = 1751
dist_trans_porto[6, 11] = 1541
dist_trans_porto[11, 6] = 1541
dist_trans_porto[6, 12] = 1950
dist_trans_porto[12, 6] = 1950

# De Rio Verde para todos os portos
dist_trans_porto[7, 10] = 2079
dist_trans_porto[10, 7] = 2079
dist_trans_porto[7, 11] = 1213
dist_trans_porto[11, 7] = 1213
dist_trans_porto[7, 12] = 2300
dist_trans_porto[12, 7] = 2300

# De São Simão para todos os portos
dist_trans_porto[8, 10] = 2298
dist_trans_porto[10, 8] = 2298
dist_trans_porto[8, 11] = 989
dist_trans_porto[11, 8] = 989
dist_trans_porto[8, 12] = 2750
dist_trans_porto[12, 8] = 2750

# De Ipameri para todos os portos
dist_trans_porto[9, 10] = 1536
dist_trans_porto[10, 9] = 1536
dist_trans_porto[9, 11] = 1034
dist_trans_porto[11, 9] = 1034
dist_trans_porto[9, 12] = 2100
dist_trans_porto[12, 9] = 2100

dist_orig_porto = {}
# De Aragarças para todos os portos
dist_orig_porto[0, 10] = 1753
dist_orig_porto[10, 0] = 1753
dist_orig_porto[0, 11] = 1354
dist_orig_porto[11, 0] = 1354
dist_orig_porto[0, 12] = 1998
dist_orig_porto[12, 0] = 1998

# De Catalão para todos os portos
dist_orig_porto[1, 10] = 1150
dist_orig_porto[10, 1] = 1150
dist_orig_porto[1, 11] = 774
dist_orig_porto[11, 1] = 774
dist_orig_porto[1, 12] = 1725
dist_orig_porto[12, 1] = 1725

# De Cristalina para todos os portos
dist_orig_porto[2, 10] = 1136
dist_orig_porto[10, 2] = 1136
dist_orig_porto[2, 11] = 957
dist_orig_porto[11, 2] = 957
dist_orig_porto[2, 12] = 1542
dist_orig_porto[12, 2] = 1542

# De Porangatu para todos os portos
dist_orig_porto[3, 10] = 1652
dist_orig_porto[10, 3] = 1652
dist_orig_porto[3, 11] = 1441
dist_orig_porto[11, 3] = 1441
dist_orig_porto[3, 12] = 1536
dist_orig_porto[12, 3] = 1536

# De Goiânia para todos os portos
dist_orig_porto[4, 10] = 1418
dist_orig_porto[10, 4] = 1418
dist_orig_porto[4, 11] = 1010
dist_orig_porto[11, 4] = 1010
dist_orig_porto[4, 12] = 1646
dist_orig_porto[12, 4] = 1646

# AQUIIII
# De Rio Verde para todos os portos
dist_orig_porto[5, 10] = 1654
dist_orig_porto[10, 5] = 1654
dist_orig_porto[5, 11] = 1594
dist_orig_porto[11, 5] = 1594
dist_orig_porto[5, 12] = 954
dist_orig_porto[12, 5] = 954


tempo_matrix = np.full((quantidade_nodes, quantidade_nodes), np.inf)

for i in N:
    for k in K:
        velocidade_media = random.uniform(50, random.choice([60, 80]))
        tempo = dist_orig_trans[i, k] / velocidade_media
        tempo_matrix[i, k] = tempo
    
    for m in M:
        velocidade_media = random.uniform(50, random.choice([60, 80]))
        tempo = dist_orig_porto[i, m] / velocidade_media
        tempo_matrix[i, m] = tempo

for k in K:
    for m in M:
        velocidade_media = random.uniform(40, 60)
        tempo = dist_trans_porto[k, m] / velocidade_media
        tempo_matrix[k, m] = tempo
                

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

# De Aragarças para cada um dos transbordos
dist_matrix[0, 6] = 408
dist_matrix[6, 0] = 408
dist_matrix[0, 7] = 372
dist_matrix[7, 0] = 372
dist_matrix[0, 8] = 523
dist_matrix[8, 0] = 523
dist_matrix[0, 9] = 588
dist_matrix[9, 0] = 588


# De Catalão para cada um dos transbordos
dist_matrix[1, 6] = 256
dist_matrix[6, 1] = 256
dist_matrix[1, 7] = 392
dist_matrix[7, 1] = 392
dist_matrix[1, 8] = 367
dist_matrix[8, 1] = 367
dist_matrix[1, 9] = 62 
dist_matrix[9, 1] = 62 

# De Cristalina para cada um dos transbordos
dist_matrix[2, 6] = 223
dist_matrix[6, 2] = 223
dist_matrix[2, 7] = 499
dist_matrix[7, 2] = 499
dist_matrix[2, 8] = 550
dist_matrix[8, 2] = 550
dist_matrix[2, 9] = 173
dist_matrix[9, 2] = 173

# De Porangatu para cada um dos transbordos
dist_matrix[3, 6] = 392
dist_matrix[6, 3] = 392
dist_matrix[3, 7] = 654
dist_matrix[7, 3] = 654
dist_matrix[3, 8] = 772
dist_matrix[8, 3] = 772
dist_matrix[3, 9] = 586
dist_matrix[9, 3] = 586

# De Goiânia para cada um dos transbordos
dist_matrix[4, 6] = 57
dist_matrix[6, 4] = 57
dist_matrix[4, 7] = 249
dist_matrix[7, 4] = 249
dist_matrix[4, 8] = 367
dist_matrix[8, 4] = 367
dist_matrix[4, 9] = 204
dist_matrix[9, 4] = 204

# De Rio Verde para cada um dos transbordos
dist_matrix[5, 6] = 450
dist_matrix[6, 5] = 450
dist_matrix[5, 7] = 0
dist_matrix[7, 5] = 0
dist_matrix[5, 8] = 138
dist_matrix[8, 5] = 138
dist_matrix[5, 9] = 520
dist_matrix[9, 5] = 520


# De Anapolis para todos os portos
dist_matrix[6, 10] = 1751
dist_matrix[10, 6] = 1751
dist_matrix[6, 11] = 1541
dist_matrix[11, 6] = 1541
dist_matrix[6, 12] = 1950
dist_matrix[12, 6] = 1950


# De Rio Verde para todos os portos
dist_matrix[7, 10] = 2079
dist_matrix[10, 7] = 2079
dist_matrix[7, 11] = 1213
dist_matrix[11, 7] = 1213
dist_matrix[7, 12] = 2300
dist_matrix[12, 7] = 2300

# De São Simão para todos os portos
dist_matrix[8, 10] = 2298
dist_matrix[10, 8] = 2298
dist_matrix[8, 11] = 989
dist_matrix[11, 8] = 989
dist_matrix[8, 12] = 2750
dist_matrix[12, 8] = 2750

# De Ipameri para todos os portos
dist_matrix[9, 10] = 1536
dist_matrix[10, 9] = 1536
dist_matrix[9, 11] = 1034
dist_matrix[11, 9] = 1034
dist_matrix[9, 12] = 2100
dist_matrix[12, 9] = 2100

# De Aragarças para todos os portos
dist_matrix[0, 10] = 1753
dist_matrix[10, 0] = 1753
dist_matrix[0, 11] = 1354
dist_matrix[11, 0] = 1354
dist_matrix[0, 12] = 1998
dist_matrix[12, 0] = 1998

# De Catalão para todos os portos
dist_matrix[1, 10] = 1150
dist_matrix[10, 1] = 1150
dist_matrix[1, 11] = 774
dist_matrix[11, 1] = 774
dist_matrix[1, 12] = 1725
dist_matrix[12, 1] = 1725

# De Cristalina para todos os portos
dist_matrix[2, 10] = 1136
dist_matrix[10, 2] = 1136
dist_matrix[2, 11] = 957
dist_matrix[11, 2] = 957
dist_matrix[2, 12] = 1542
dist_matrix[12, 2] = 1542

# De Porangatu para todos os portos
dist_matrix[3, 10] = 1652
dist_matrix[10, 3] = 1652
dist_matrix[3, 11] = 1441
dist_matrix[11, 3] = 1441
dist_matrix[3, 12] = 1536
dist_matrix[12, 3] = 1536

# De Goiânia para todos os portos
dist_matrix[4, 10] = 1418
dist_matrix[10, 4] = 1418
dist_matrix[4, 11] = 1010
dist_matrix[11, 4] = 1010
dist_matrix[4, 12] = 1646
dist_matrix[12, 4] = 1646

# AQUIIII
# De Rio Verde para todos os portos
dist_matrix[5, 10] = 1654
dist_matrix[10, 5] = 1654
dist_matrix[5, 11] = 1594
dist_matrix[11, 5] = 1594
dist_matrix[5, 12] = 954
dist_matrix[12, 5] = 954


range_trans = len(N)
range_port = len(N) + len(K)
range_client = len(N) + len(K) + len(M)


cr = 15.42

# Custo do transporte ferroviário
cf = 7.03

# Custo da multimodalidade
ci = 0.09

# Emissão do transporte rodoviário
er = 52.77 

# Emissão do transporte ferroviário
ef = 18.05









# dist_matrix =
# dist_matrix = 
# dist_orig_porto =
