"""O problema da mochila: um problema de otimização combinatória.
O nome dá-se devido ao modelo de uma situação em que é necessário
preencher uma mochila com objetos de diferentes pesos e valores.
O objetivo é que se preencha a mochila com o maior valor possível,
não ultrapassando o peso máximo."""

from gen_alg import *
from draw_methods import *
import random

# [peso,valor]
# itens_disponiveis = [[4, 30], [8, 10], [8, 30], [25, 75],
#                    [2, 10], [50, 100], [6, 300], [12, 50],
#                    [100, 400], [8, 300]]
# gera o conjunto de itens de forma aleatória. Gera 20 itens com peso entre 1 e 10 e valor entre 1 e 300
itens_disponiveis = [(random.randint(1, 10), random.randint(1, 300)) for _ in range(20)]

peso_maximo = 100
tamanho_populacao = 150
max_geracoes = 200
qtd_itens_disponiveis = len(itens_disponiveis)

running = True
cont_geracao = 0

populacao = population(tamanho_populacao, qtd_itens_disponiveis)
historico_de_fitness = [media_fitness(populacao, peso_maximo, itens_disponiveis)]

mutate = 0.05


def inverter_array(array):
    return array[::-1]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False  # Quit the game when the 'q' key is pressed

    if cont_geracao < max_geracoes:

        pais = [[fitness(x, peso_maximo, itens_disponiveis), x] for x in populacao if
                fitness(x, peso_maximo, itens_disponiveis) >= 0]
        pais.sort(reverse=True)

        # REPRODUCAO
        filhos = []
        while len(filhos) < tamanho_populacao:
            homem, mulher = selecao_roleta(pais)
            meio = len(homem) // 2
            filho = homem[:meio] + mulher[meio:]
            filhos.append(filho)

        # MUTACAO
        for individuo in filhos:
            if mutate > random.random():
                pos_to_mutate = randint(0, len(individuo) - 1)
                if individuo[pos_to_mutate] == 1:
                    individuo[pos_to_mutate] = 0
                else:
                    individuo[pos_to_mutate] = 1

        populacao = filhos

        historico_de_fitness.append(media_fitness(populacao, peso_maximo, itens_disponiveis))
        cont_geracao += 1

        historico_de_fitness_invertido = inverter_array(historico_de_fitness)
        draw_plot(list(range(len(historico_de_fitness))), historico_de_fitness)

        draw_text(screen, f'Melhor resultado: {"{:.2f}".format(max(historico_de_fitness))}',
                  930, window_size[1] - 100, font_size=25, font='Arial')

        tick_clock()
    else:
        running = False
        #quit_pygame()

# PRINTS DO TERMINAL
for indice, dados in enumerate(historico_de_fitness):
    print("Geracao: ", indice, " | Media de valor na mochila: ", dados)

print("\nPeso máximo:", peso_maximo, "g\n\nItens disponíveis:")
for indice, i in enumerate(itens_disponiveis):
    print("Item ", indice + 1, ": ", i[0], "g | R$", i[1])

print("\nExemplos de boas solucoes: ")
for i in range(5):
    print(populacao[i])

k = input("press close to exit")