from modelo_gurobi import Gurobi
from genetico import Evolution
import pandas as pd
import json

nome = "Plot"
list_resul = []

df = pd.DataFrame()
seila = Gurobi()

# valor_f1, valor_f2 = seila.otimizar()
# if valor_f1 != 0:
#     df = df.append(
#         {"Custo Transporte": valor_f1, "Emissão Transporte": valor_f2},
#         ignore_index=True,
#     )

# df.to_csv("resultados_" + nome + "_gurobi.csv")

otmz = Evolution("Plot", 0)
front = otmz.evolve()
texto = ""

arquivo = open("rotas_resul_Plot.txt", "a")
for cont, eita in enumerate(front.fronts[0]):
    arquivo.write("individuo_" + str(cont) + "\n")
    for k in range(1):
        d = dict(eita.cromossomos[k].lista_adjacencia)
        arquivo.write("Cliente_" + str(k) + ":  ")
        arquivo.write(json.dumps(d) + "\n")

arquivo.close()


breakpoint()
