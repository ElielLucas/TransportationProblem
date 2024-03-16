import numpy as np

import input as inp
from typing import List, Dict, DefaultDict, Set
from collections import defaultdict
from random import random


class Individuo:
    def __init__(self) -> None:
        self.num_itens = inp.setup["N_ITENS"]
        self.valores_itens = inp.setup["VALORES"]
        self.pesos_itens = inp.setup["PESOS"]

        self.itens_escolhidos = []

        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        self.features = None

        self.montar_solução_random()
        self.calculate_objectives()

    def __lt__(self, other):
        return (self.of[0] < other.of[0] and self.of[1] <= other.of[1]) or (
            self.of[0] <= other.of[0] and self.of[1] < other.of[1]
        )

    def montar_solução_random(self):
        for _ in range(self.num_itens):
            self.itens_escolhidos.append(1 if random() > 0.5 else 0)


    def dominates(self, other_individual):
        and_condition = True
        or_condition = False
        for first, second in zip(self.of, other_individual.of):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return and_condition and or_condition

    def objective_function(self):
        valor_total = 0
        peso_total = 0
        for i in range(self.num_itens):
            valor_total += self.valores_itens[i] * self.itens_escolhidos[i] * random()
            peso_total += self.pesos_itens[i] * self.itens_escolhidos[i] 

            # valor_total -= 5 * peso_total

        return [valor_total, peso_total]

    def calculate_objectives(self):
        self.of = self.objective_function()
        self.fit = self.calculate_fit(self.of)
        
        # Conflito: Ativa o modo de inversão se a aptidão do peso for maior que a do valor
        if self.fit[1] > self.fit[0]:
            self.modo_inverter = True
        else:
            self.modo_inverter = False

    def calculate_fit(self, of):
        of_valor, of_peso = of

        if of_valor >= 0:
            fit_valor = 1 + of_valor
        else:
            fit_valor = 1 / (1 + abs(of_valor))

        if of_peso >= 0:
            fit_peso = 1 / (1 + of_peso) 
        else:
            fit_peso = 1 + abs(of_peso)

        return [fit_valor, fit_peso]
