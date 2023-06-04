import math
import numpy as np

dist_matrix = np.array([
    [3, 4, 5],
    [10, 8, 20],
])

def find_nearest_neighbor(ponto_referencia, ponto_proibido):
    vizinho_mais_proximo = float('inf')
    indice_vizinho_mais_proximo = None

    for i, distancia in enumerate(dist_matrix[ponto_referencia]):
        if ponto_proibido != i and distancia < vizinho_mais_proximo:
            vizinho_mais_proximo = distancia
            indice_vizinho_mais_proximo = i

    return indice_vizinho_mais_proximo

# Definir função para aplicar a heurística de inserção em uma solução
def insercao_heuristica(solucao, capacidade_ferroviaria):
    # Realizar uma cópia da solução para não modificar a original
    nova_solucao = solucao.copy()
    
    # Iterar sobre os pontos ferroviários
    for ponto_ferroviario in range(len(capacidade_ferroviaria)):
        carga_total = sum(nova_solucao[ponto_ferroviario::len(capacidade_ferroviaria)])  # Calcular a carga total no ponto ferroviário
        # Verificar se a carga total excede a capacidade do ponto ferroviário
        if carga_total > capacidade_ferroviaria[ponto_ferroviario]:
            excesso_carga = carga_total - capacidade_ferroviaria[ponto_ferroviario]

            # Iterar sobre os produtores
            for i, produtor in enumerate(range(ponto_ferroviario, len(nova_solucao), len(capacidade_ferroviaria))):
                # Verificar se o produtor tem carga para realocar
                if nova_solucao[produtor] > 0:
                    quantidade_realocar = min(nova_solucao[produtor], excesso_carga)  # Calcular a quantidade de carga a ser realocada

                # Encontrar o ponto ferroviário mais próximo com capacidade disponível
                ferro_mais_proxima = find_nearest_neighbor(i, ponto_ferroviario)
                destino = ferro_mais_proxima + i * len(capacidade_ferroviaria)
    
                if carga_total - nova_solucao[produtor] + quantidade_realocar <= capacidade_ferroviaria[destino % len(capacidade_ferroviaria)]:
                    nova_solucao[produtor] -= quantidade_realocar
                    nova_solucao[destino] += quantidade_realocar
                    excesso_carga -= quantidade_realocar
                    carga_total -= quantidade_realocar
                
                if excesso_carga <= 0:
                    break

    return nova_solucao



# ponto_referencia = 0
# vizinho_mais_proximo = find_nearest_neighbor(dist_matrix, ponto_referencia)
# print("O vizinho mais próximo do ponto de referência", ponto_referencia, "é o ponto", vizinho_mais_proximo)


# Exemplo de uso da heurística de inserção

solucao_inicial = [10, 15, 20, 10, 5, 50]  # Exemplo simplificado com 2 produtores e 3 pontos ferroviários
capacidade_ferroviaria = [15, 200, 20]  # Capacidade de cada ponto ferroviário
demanda_clientes = [15, 25]  # Demanda de cada cliente

# # Aplicar a heurística de inserção na solução inicial
nova_solucao = insercao_heuristica(solucao_inicial, capacidade_ferroviaria)

breakpoint()
# # Imprimir a nova solução
# print("Solução inicial:", solucao_inicial)
# print("Nova solução:", nova_solucao)