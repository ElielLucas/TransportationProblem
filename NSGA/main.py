from modelo_gurobi import Gurobi
from evolution import Evolution
from defines import Defines
import pandas as pd
import random

nome = 'instancias_pequenas'
# list_resul = []
# df = pd.DataFrame()
# for i in range(14, 15):
#     seila = Gurobi(nome, i, 2000, 80, 1000, 3000)
#     valor_f1, valor_f2 = seila.otimizar()
#     if valor_f1 != 0:
#         df = df.append({'Custo Transporte': valor_f1, 'Emissão Transporte': valor_f2}, ignore_index=True)

# df.to_csv('resultados_' + nome + '_gurobi.csv')

for i in range(0, 10):
    for i in range(14, 15):
        otmz = Evolution(nome, i)
        front = otmz.evolve()
    breakpoint()


    
