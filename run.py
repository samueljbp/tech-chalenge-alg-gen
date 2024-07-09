from gen_alg import *
from draw_methods import *
import random

# cores dos textos da exibição da solução
COR_VERDE_ESCURO = (0, 100, 0)
COR_VERMELHO_ESCURO = (139, 0, 0)
COR_AZUL_ESCURO = (0, 0, 139)

# gera o conjunto de itens de forma aleatória. Gera 20 itens com peso entre 1 e 10 e valor entre 1 e 300
itens_disponiveis = [(random.randint(5, 10), random.randint(1, 300)) for _ in range(16)]

peso_maximo = 40 # peso máximo da mochila
tamanho_populacao = 150 # tamanho da população de cada geração
max_geracoes = 200 # numero máximo de gerações que serão executadas
qtd_itens_disponiveis = len(itens_disponiveis) # quantidade de itens disponíveis
geracoes_estagnacao = 50 # quantidade de gerações a se passarem sem melhora do fitness para que o algoritmo seja considerado estagnado

running = True # indica se o algoritmo está rodando
cont_geracao = 0 # indica a geração atual
cont_estagnacao = 0 # quantidade de gerações que se passaram sem melhoria do fitness

populacao = population(tamanho_populacao, qtd_itens_disponiveis) # armazena a população de cada geração
melhor_sol_geracao = melhor_solucao(populacao, peso_maximo, itens_disponiveis) # armazena a melhor solução da geração atual
historico_de_solucoes = [(0, [])] # armazena todas as soluções
melhor_sol_historica = [] # armazena a melhor solução entre todas as gerações

melhor_fitness_anterior = 0 # variável auxiliar para controlar se o fitness melhorou em relação à geração anterior

mutation_probability = 0.05 # propoabilidade de um indivíduo sofrer mutação

elitismo = True # indica se o algoritmo vai trabalhar com ou sem elitismo

# loop principal do algoritmo
while running:
    # trata condições para finalizar a execução
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False  # fecha o pygame quabndo a tecla 'q' for pressionada

    # executa a evolução caso esteja dentro do limite de gerações ou se o algoritmo não tiver estagnado
    if cont_geracao < max_geracoes and cont_estagnacao < geracoes_estagnacao:

        # armazena os pais e seus respectivos fitness para trabalhar
        pais = [[fitness(x, peso_maximo, itens_disponiveis), x] for x in populacao if
                fitness(x, peso_maximo, itens_disponiveis) >= 0]
        # inverte a ordem do array
        pais.sort(reverse=True)

        # gera a nova população de indivíduos
        filhos = reproduce(pais, tamanho_populacao, "R", elitismo, melhor_sol_historica)

        # realiza mutação dos indivíduos (mantem o melhor indivíduo intacto caso esteja trabalhando com elitismo)
        for ind, individuo in enumerate(filhos):
            if ind > 0 or not elitismo:
                mutate(mutation_probability, individuo)

        # substitui a população anterior pelos novos indivíduos
        populacao = filhos

        # Identifica melhor solução da geração
        melhor_sol_geracao = melhor_solucao(populacao, peso_maximo, itens_disponiveis)
        print("Melhor sol", melhor_sol_geracao)

        # atualiza a variável de melhor solução histórica caso necessário
        fit_melhor_sol_hist = fitness(melhor_sol_historica, peso_maximo, itens_disponiveis)
        if melhor_sol_geracao[0] > fit_melhor_sol_hist:
            melhor_sol_historica = melhor_sol_geracao[1]

        # atualiza o contador de estagnação
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
