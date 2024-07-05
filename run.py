from gen_alg import *
from draw_methods import *
import random

COR_VERDE_ESCURO = (0, 100, 0)
COR_VERMELHO_ESCURO = (139, 0, 0)
COR_AZUL_ESCURO = (0, 0, 139)

# gera o conjunto de itens de forma aleatória. Gera 20 itens com peso entre 1 e 10 e valor entre 1 e 300
itens_disponiveis = [(random.randint(5, 10), random.randint(1, 300)) for _ in range(16)]

peso_maximo = 40
tamanho_populacao = 150
max_geracoes = 200
qtd_itens_disponiveis = len(itens_disponiveis)
geracoes_estagnacao = 50

running = True
cont_geracao = 0
cont_estagnacao = 0

populacao = population(tamanho_populacao, qtd_itens_disponiveis)
melhor_sol = melhor_solucao(populacao, peso_maximo, itens_disponiveis)
historico_de_fitness = [melhor_sol[0]]
historico_de_solucoes = [melhor_sol[1]]

melhor_fitness_anterior = 0

mutation_probability = 0.05

elitismo = True


def inverter_array(array):
    return array[::-1]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False  # Quit the game when the 'q' key is pressed

    if cont_geracao < max_geracoes and cont_estagnacao < geracoes_estagnacao:

        pais = [[fitness(x, peso_maximo, itens_disponiveis), x] for x in populacao if
                fitness(x, peso_maximo, itens_disponiveis) >= 0]
        pais.sort(reverse=True)

        # Identificar melhor solução entre todas as gerações para exibir
        indice_melhor_sol_historica = historico_de_fitness.index(max(historico_de_fitness))
        melhor_sol_historica = historico_de_solucoes[indice_melhor_sol_historica]

        # REPRODUCAO
        filhos = reproduce(pais, tamanho_populacao, "R", elitismo, melhor_sol_historica)

        # MUTACAO
        for individuo in filhos:
            mutate(mutation_probability, individuo)

        populacao = filhos

        # Identifica melhor solução da geração
        melhor_sol = melhor_solucao(populacao, peso_maximo, itens_disponiveis)

        if melhor_sol[0] > melhor_fitness_anterior:
            melhor_fitness_anterior = melhor_sol[0]
            cont_estagnacao = 0
        else:
            cont_estagnacao += 1

        historico_de_fitness.append(melhor_sol[0])
        historico_de_solucoes.append(melhor_sol[1])
        cont_geracao += 1

        historico_de_fitness_invertido = inverter_array(historico_de_fitness)
        draw_plot(list(range(len(historico_de_fitness))), historico_de_fitness)

        draw_text(screen, "Exemplo de solução",
                  930, 20, (0, 0, 0), font_size=20, font='Arial')        

        y_item = 60
        for indice, item in enumerate(itens_disponiveis):
            cor = COR_VERMELHO_ESCURO
            if melhor_sol_historica[indice] == 1:
                cor = COR_VERDE_ESCURO
            draw_text(screen, "Item " + str(indice) + " - " + str(item[0]) + " g | R$ " + str(item[1]),
                      930, y_item, cor, font_size=15, font='Arial')
            y_item += 30

        draw_text(screen, f'Melhor resultado: R$ {"{:.2f}".format(max(historico_de_fitness))}',
                  930, window_size[1] - 50, font_size=22, font='Arial')

        tick_clock()
    else:
        running = False

        if cont_estagnacao >= geracoes_estagnacao:
            # estagnou
            draw_text(screen, "Estagnou!",
                      1080, 60, COR_AZUL_ESCURO, font_size=20, font='Arial')

            tick_clock()

        #quit_pygame()

k = input("press close to exit")
