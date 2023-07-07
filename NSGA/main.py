from modelo_gurobi import Gurobi
import pandas as pd

# nome = 'instancias_pequenas'
# list_resul = []
# df = pd.DataFrame()
# # for i in range(1):
# seila = Gurobi(nome, 0, 100, 8, 10, 800)
# valor_f1, valor_f2 = seila.otimizar()
# if valor_f1 != 0:
#     df = df.append({'Custo Transporte': valor_f1, 'Emissão Transporte': valor_f2}, ignore_index=True)

# df.to_csv('resultados_' + nome + '_gurobi.csv')


    
dados = pd.read_csv('testes_mono_objetivo/resultados_teste8.csv')
breakpoint()
