

import pandas as pd


df = pd.read_csv('resultados_teste9.csv')
valor1 = df['Inst.Pequena - 3'].mean()
valor2 = 2.95923033e+08


gap = ((valor1 - valor2)/valor1) * 100

print(gap)