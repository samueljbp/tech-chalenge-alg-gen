"""O problema da mochila: um problema de otimização combinatória.
O nome dá-se devido ao modelo de uma situação em que é necessário
preencher uma mochila com objetos de diferentes pesos e valores.
O objetivo é que se preencha a mochila com o maior valor possível,
não ultrapassando o peso máximo."""

from gen_alg import *
import random
import pygame

# [peso,valor]
# itens_disponiveis = [[4, 30], [8, 10], [8, 30], [25, 75],
#                    [2, 10], [50, 100], [6, 300], [12, 50],
#                    [100, 400], [8, 300]]
itens_disponiveis = [(random.randint(1, 10), random.randint(1, 300)) for _ in range(20)]

peso_maximo = 100
tamanho_populacao = 150
max_geracoes = 80
qtd_itens_disponiveis = len(itens_disponiveis)

running = True
cont_geracao = 0

# EXECUCAO DOS PROCEDIMENTOS
populacao = population(tamanho_populacao, qtd_itens_disponiveis)
historico_de_fitness = [media_fitness(populacao, peso_maximo, itens_disponiveis)]
for i in range(max_geracoes):
    populacao = evolve(populacao, peso_maximo, itens_disponiveis, tamanho_populacao)
    historico_de_fitness.append(media_fitness(populacao, peso_maximo, itens_disponiveis))

# PRINTS DO TERMINAL
for indice, dados in enumerate(historico_de_fitness):
    print("Geracao: ", indice, " | Media de valor na mochila: ", dados)

print("\nPeso máximo:", peso_maximo, "g\n\nItens disponíveis:")
for indice, i in enumerate(itens_disponiveis):
    print("Item ", indice + 1, ": ", i[0], "g | R$", i[1])

print("\nExemplos de boas solucoes: ")
for i in range(5):
    print(populacao[i])

# GERADOR DE GRAFICO
from matplotlib import pyplot as plt

plt.plot(range(len(historico_de_fitness)), historico_de_fitness)
plt.grid(True, zorder=0)
plt.title("Problema da mochila")
plt.xlabel("Geracao")
plt.ylabel("Valor medio da mochila")
plt.show()