from modelo_gurobi import Gurobi

nome = 'instancia_pequena'
i = 1
seila = Gurobi(nome, i, 20, 5, 10, 60)
seila.otimizar()
breakpoint()