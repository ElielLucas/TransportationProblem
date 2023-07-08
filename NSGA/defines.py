import numpy as np
from utils import gen_points
import random

class Defines:
    def __init__(self, nome_instancia, iteracao):
        self.nome_instancia = nome_instancia
        self.iteracao = iteracao
        self.er = 0.8
        self.ef = 0.2
        with open(self.nome_instancia + str(self.iteracao) + '.txt', 'r') as arquivo:
            linhas = arquivo.readlines()
            self.cr = float(linhas[0].rstrip('\n'))
            self.cf = float(linhas[1].rstrip('\n'))
            self.N = linhas[2].split()
            self.N = [int(valor) for valor in self.N if valor != '\n']
            self.K = linhas[3].split()
            self.K = [int(valor) for valor in self.K if valor != '\n']
            self.M = linhas[4].split()
            self.M = [int(valor) for valor in self.M if valor != '\n']
            self.demandas = linhas[5].split()
            self.demandas = [int(valor) for valor in self.demandas if valor != '\n']
            # breakpoint()
            self.demandas_clientes = [sum(self.demandas)]
            
            self.ofertas = linhas[6].split()
            self.ofertas = [int(valor) for valor in self.ofertas if valor != '\n']
            
            self.capacidade_ferrovias = linhas[7].split()
            self.capacidade_ferrovias = [int(valor) for valor in self.capacidade_ferrovias if valor != '\n']
            
            self.capacidade_portos = linhas[8].split()
            self.capacidade_portos = [int(valor) for valor in self.capacidade_portos if valor != '\n']

            self.points_orig = []
            self.points_trans = []
            self.points_portos = []

            for it, i in enumerate(range(9, len(linhas))):
                if it in self.N:
                    pontos = linhas[i].split()
                    pontos = [int(valor) for valor in pontos if valor != '\n']
                    self.points_orig.append(pontos)
                elif it in self.K:
                    pontos = linhas[i].split()
                    pontos = [int(valor) for valor in pontos if valor != '\n']
                    self.points_trans.append(pontos)
                else:
                    pontos = linhas[i].split()
                    pontos = [int(valor) for valor in pontos if valor != '\n']
                    self.points_portos.append(pontos)

        self.range_trans = len(self.N)
        self.range_port = len(self.N) + len(self.K)

        self.quantidade_nodes = len(self.N) + len(self.K) + len(self.M)
        self.tempo_matrix = np.full((self.quantidade_nodes, self.quantidade_nodes), np.inf)

        with open(self.nome_instancia + str(self.iteracao) + '_tempo.txt', 'r') as arquivo:
            linhas = arquivo.readlines()
            aux = 0
            for it, i in enumerate(range(0, len(linhas))):
                if it in self.N:
                    pontos = linhas[i].split()
                    for it2, tempo in enumerate(pontos):
                        self.tempo_matrix[it][self.K[it2]] = tempo
                elif it in self.K:
                    pontos = linhas[i].split()
                    for it2, tempo in enumerate(pontos):
                        self.tempo_matrix[it][self.M[it2]] = tempo
                else:
                    pontos = linhas[i].split()
                    for it2, tempo in enumerate(pontos):
                        self.tempo_matrix[aux][self.M[it2]] = tempo
                    aux += 1
            
        self.dist_matrix = np.full((self.quantidade_nodes, self.quantidade_nodes), np.inf)
        for i in self.N:
            for k in self.K:
                distancia = gen_points.distance(self.points_orig[i][0], self.points_orig[i][1], self.points_trans[k - self.range_trans][0], self.points_trans[k - self.range_trans][1])
                self.dist_matrix[i, k] = self.dist_matrix[k, i] = distancia
            
            for m in self.M:
                distancia = gen_points.distance(self.points_orig[i][0], self.points_orig[i][1], self.points_portos[m - self.range_port][0], self.points_portos[m - self.range_port][1])
                self.dist_matrix[i, m] = self.dist_matrix[m, i] = distancia

        for k in self.K:
            for m in self.M:
                distancia = gen_points.distance(self.points_trans[k - self.range_trans][0], self.points_trans[k - self.range_trans][1], self.points_portos[m - self.range_port][0], self.points_portos[m - self.range_port][1])
                self.dist_matrix[k, m] = self.dist_matrix[m, k] = distancia
