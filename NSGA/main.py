from modelo_gurobi import Gurobi
from evolution import Evolution
from defines import Defines
import pandas as pd
import random
from collections import defaultdict
import json
import input as inp

nome = 'instancias_pequenas'
list_resul = []
df = pd.DataFrame()
for i in range(10, 11):
    seila = Gurobi()
    valor_f1, valor_f2 = seila.otimizar()
    if valor_f1 != 0:
        df = df.append({'Custo Transporte': valor_f1, 'Emissão Transporte': valor_f2}, ignore_index=True)

df.to_csv('resultados_' + nome + '_gurobi.csv')


for i in range(10, 11):
    otmz = Evolution('caso_teste', i)
    front = otmz.evolve()
    texto = ''

    arquivo = open("rotas_resul_3.txt", "a")
    for cont, eita in enumerate(front.fronts[0]):
        arquivo.write("individuo_"+str(cont)+'\n')
        for k in range(1):
            d = dict(eita.cromossomos[k].lista_adjacencia)
            arquivo.write("Cliente_" + str(k) + ':  ')
            arquivo.write(json.dumps(d) + "\n")
    
    arquivo.close()


#     df = pd.DataFrame()
#     for i in range(len(front)):
#         df = df.append({'Custo Transporte': front[i].of[0], 'Emissão Transporte': front[i].of[1]}, ignore_index=True)
    
#     df.to_csv('resultados_' + nome + str(i) + '_NSGA.csv')


    
