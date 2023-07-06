from modelo_gurobi import Gurobi
from evolution import Evolution
from defines import Defines
import pandas as pd
import random

nome = 'instancias_pequenas'
# list_resul = []
# df = pd.DataFrame()
# for i in range(10):
#     num_ori = random.randint(1, 20)
#     num_trans = random.randint(1, 5)
#     num_port = random.randint(1, 10)
#     num_cli = random.randint(1, 60)
#     # while num_ori * num_trans * num_port * num_cli > 16800000:
#     #     num_ori = random.randint(1, 100)
#     #     num_trans = random.randint(1, 20)
#     #     num_port = random.randint(1, 30)
#     #     num_cli = random.randint(1, 600)
#     seila = Gurobi(nome, i, num_ori, num_trans, num_port, num_cli)
#     valor_f1, valor_f2 = seila.otimizar()
#     if valor_f1 != 0:
#         df = df.append({'Custo Transporte': valor_f1, 'Emissão Transporte': valor_f2}, ignore_index=True)

# df.to_csv('resultados_' + nome + '_gurobi.csv')

for i in range(1):
    otmz = Evolution(nome, i)
    front = otmz.evolve()
    df = pd.DataFrame()
    for i in range(len(front)):
        df = df.append({'Custo Transporte': front[i].of[0], 'Emissão Transporte': front[i].of[1]})
    
    df.to_csv('resultados_' + nome + str(i) + '_NSGA.csv')
    
