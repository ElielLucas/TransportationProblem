from modelo_gurobi import Gurobi
from genetico import Evolution
from random import random, randint
import pandas as pd
import json
import input as inp

nome = "Plot"

num_itens = 4000
valores_itens = [randint(10, 1000) for _ in range(num_itens)]
pesos_itens = [randint(1, 50) for _ in range(num_itens)]
# valores_itens = [1000, 2, 30, 400, 15]
# pesos_itens = [200, 1, 10, 20, 50]

setup = {
    "N_ITENS": num_itens,
    "VALORES": valores_itens,
    "PESOS": pesos_itens
}

inp.setup = setup

otmz = Evolution("Plot")
front = otmz.evolve()

arquivo = open("rotas_resul_Plot.txt", "a")
for cont, eita in enumerate(front.fronts[0]):
    arquivo.write("individuo_" + str(cont) + "\n")
    for k in range(1):
        d = dict(eita.cromossomos[k].lista_adjacencia)
        arquivo.write("Cliente_" + str(k) + ":  ")
        arquivo.write(json.dumps(d) + "\n")

arquivo.close()


breakpoint()
