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
melhor_sol_geracao = melhor_solucao(populacao, peso_maximo, itens_disponiveis)
historico_de_solucoes = [(0, [])]
melhor_sol_historica = []

melhor_fitness_anterior = 0

mutation_probability = 0.05

elitismo = False


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

        # REPRODUCAO
        filhos = reproduce(pais, tamanho_populacao, "R", elitismo, melhor_sol_historica)

        # MUTACAO
        for individuo in filhos:
            mutate(mutation_probability, individuo)

        populacao = filhos

        # Identifica melhor solução da geração
        melhor_sol_geracao = melhor_solucao(populacao, peso_maximo, itens_disponiveis)
        print("Melhor sol", melhor_sol_geracao)

        fit_melhor_sol_hist = fitness(melhor_sol_historica, peso_maximo, itens_disponiveis)
        if melhor_sol_geracao[0] > fit_melhor_sol_hist:
            melhor_sol_historica = melhor_sol_geracao[1]

        if melhor_sol_geracao[0] > melhor_fitness_anterior:
            melhor_fitness_anterior = melhor_sol_geracao[0]
            cont_estagnacao = 0
        else:
            cont_estagnacao += 1

        historico_de_solucoes.append(melhor_sol_geracao)
        cont_geracao += 1

        hist_fit = []
        for item in historico_de_solucoes:
            hist_fit.append(item[0])
        draw_plot(list(range(len(hist_fit))), hist_fit)

        draw_text(screen, "Exemplo de solução",
                  930, 20, (0, 0, 0), font_size=20, font='Arial')

        y_item = 60
        for i, item in enumerate(itens_disponiveis):
            cor = COR_VERMELHO_ESCURO
            if melhor_sol_historica[i] == 1:
                cor = COR_VERDE_ESCURO
            print ("item", i, item, melhor_sol_historica[i])
            draw_text(screen, "Item " + str(i + 1) + " - " + str(item[0]) + " g | R$ " + str(item[1]),
                      930, y_item, cor, font_size=15, font='Arial')
            y_item += 30

        draw_text(screen, f'Melhor resultado: R$ {"{:.2f}".format(fitness(melhor_sol_historica,peso_maximo, itens_disponiveis))}',
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

print("Melhor solucao historica", melhor_sol_historica, fitness(melhor_sol_historica, peso_maximo, itens_disponiveis))

k = input("press close to exit")
