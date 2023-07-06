from modelo_gurobi import Gurobi
from evolution import Evolution
from defines import Defines
import pandas as pd

nome = 'instancias_pequenas'
# list_resul = []
# df = pd.DataFrame()
# for i in range(10):
#     seila = Gurobi(nome, i, 20, 5, 10, 60)
#     valor_f1, valor_f2 = seila.otimizar()
#     if valor_f1 != 0:
#         df = df.append({'Custo Transporte': valor_f1, 'Emissão Transporte': valor_f2}, ignore_index=True)

# df.to_csv('resultados_' + nome + '_gurobi.csv')

for i in range(10):
    otmz = Evolution(nome, i)
    front = otmz.evolve()
    df = pd.DataFrame()
    for i in range(len(front)):
        df = df.append({'Custo Transporte': front[i].of[0], 'Emissão Transporte': front[i].of[1]})
    
    df.to_csv('resultados_' + nome + str(i) + '_NSGA.csv')
    
