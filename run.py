"""O problema da mochila: um problema de otimização combinatória.
O nome dá-se devido ao modelo de uma situação em que é necessário
preencher uma mochila com objetos de diferentes pesos e valores.
O objetivo é que se preencha a mochila com o maior valor possível,
não ultrapassando o peso máximo."""

from gen_alg import *
from draw_methods import *
import random

COR_VERDE_ESCURO = (0, 100, 0)
COR_VERMELHO_ESCURO = (139, 0, 0)

# [peso,valor]
# itens_disponiveis = [[4, 30], [8, 10], [8, 30], [25, 75],
#                    [2, 10], [50, 100], [6, 300], [12, 50],
#                    [100, 400], [8, 300]]
# gera o conjunto de itens de forma aleatória. Gera 20 itens com peso entre 1 e 10 e valor entre 1 e 300
itens_disponiveis = [(random.randint(1, 10), random.randint(1, 300)) for _ in range(16)]

peso_maximo = 30
tamanho_populacao = 150
max_geracoes = 200
qtd_itens_disponiveis = len(itens_disponiveis)

running = True
cont_geracao = 0

populacao = population(tamanho_populacao, qtd_itens_disponiveis)
melhor_sol = melhor_solucao(populacao, peso_maximo, itens_disponiveis)
historico_de_fitness = [melhor_sol[0]]
historico_de_solucoes = [melhor_sol[1]]

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
            pai1, pai2 = selecao_roleta(pais)
            meio = len(pai1) // 2
            filho = pai1[:meio] + pai2[meio:]
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

        # historico_de_fitness.append(media_fitness(populacao, peso_maximo, itens_disponiveis))
        melhor_sol = melhor_solucao(populacao, peso_maximo, itens_disponiveis)
        print("Melhor fit", str(melhor_sol[0]))
        print("Melhor sol", str(melhor_sol[1]))
        # print("Historico", historico_de_fitness)
        historico_de_fitness.append(melhor_sol[0])
        historico_de_solucoes.append(melhor_sol[1])
        cont_geracao += 1

        historico_de_fitness_invertido = inverter_array(historico_de_fitness)
        draw_plot(list(range(len(historico_de_fitness))), historico_de_fitness)

        draw_text(screen, "Melhor conjunto de itens",
                  930, 20, (0, 0, 0), font_size=20, font='Arial')

        y_item = 60
        for indice, item in enumerate(itens_disponiveis):
            cor = COR_VERMELHO_ESCURO
            if melhor_sol[1][indice] == 1:
                cor = COR_VERDE_ESCURO
            draw_text(screen, "Item " + str(indice) + " - " + str(item[0]) + " g | R$ " + str(item[1]),
                      930, y_item, cor, font_size=15, font='Arial')
            y_item += 30

        draw_text(screen, f'Melhor resultado: {"{:.2f}".format(max(historico_de_fitness))}',
                  930, window_size[1] - 50, font_size=25, font='Arial')

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
