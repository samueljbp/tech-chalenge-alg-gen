import random


def create_individual(n_de_itens):
    # cria um indivíduo aleatoriamente com um bit 1/0 para cada posição com o tamanho da lista de itens
    return [random.getrandbits(1) for x in range(n_de_itens)]


def population(n_de_individuos, n_de_itens):
    # cria a popupalação, respeitando a variável que define o tamanho da mesma
    return [create_individual(n_de_itens) for x in range(n_de_individuos)]


def reproduce(pais, tamanho_populacao, tecnica_selecao = "T", elitismo=True, melhor_individuo=None):
    filhos = []

    if elitismo and melhor_individuo is not None:
        # Mantém o melhor indivíduo se estiver configurado para tal
        filhos.append(melhor_individuo)

    # se estiver parametrizado para fazer seleção por torneio
    if tecnica_selecao == "T":
        tamanho_torneio = 10
        while len(filhos) < tamanho_populacao:
            pai1_genes = selecao_torneio(pais, tamanho_torneio)
            pai2_genes = selecao_torneio(pais, tamanho_torneio)

            # Cruzamento de Um Ponto
            meio = len(pai1_genes) // 2
            filho_genes = pai1_genes[:meio] + pai2_genes[meio:]
            filhos.append(filho_genes)
    
    # se estiver parametrizado para fazer seleção por roleta
    if tecnica_selecao == "R":
        while len(filhos) < tamanho_populacao:
            # seleciona os pais por roleta
            pai1, pai2 = selecao_roleta(pais)

            # Cruzamento de Um Ponto
            meio = len(pai1) // 2
            filho = pai1[:meio] + pai2[meio:]
            filhos.append(filho)

    return filhos


def mutate(mutation_probability, individuo):
    # gera um numero aleatório e se ele for menor que a probabilidade, faz a mutanção
    if mutation_probability > random.random():
        # técnica Mutação de Bit
        pos_to_mutate = random.randint(0, len(individuo) - 1)
        if individuo[pos_to_mutate] == 1:
            individuo[pos_to_mutate] = 0
        else:
            individuo[pos_to_mutate] = 1

    return individuo


def fitness(individuo, peso_maximo, itens_disponiveis):
    # calcula o fitness e o peso do indivíduo somando o valor dos seus itens que tem valor 1
    peso_total, valor_total = 0, 0
    for indice, valor in enumerate(individuo):
        peso_total += (individuo[indice] * itens_disponiveis[indice][0])
        valor_total += (individuo[indice] * itens_disponiveis[indice][1])

    if (peso_maximo - peso_total) < 0:
        return -1  # retorna -1 no caso de peso excedido, desconsiderando este indivíduo

    return valor_total  # se for um individuo valido retorna seu valor, sendo maior melhor


def melhor_solucao(populacao, peso_maximo,
                   itens_disponiveis):  # só leva em consideracao os elementos que respeitem o peso maximo da mochila
    # encontra o indivíduo de maior fitness da popupação
    melhor_fit = 0
    melhor_sol = ()
    for x in populacao:
        fit = fitness(x, peso_maximo, itens_disponiveis)
        if fit > melhor_fit:
            melhor_fit = fit
            melhor_sol = x

    return melhor_fit, melhor_sol


def selecao_torneio(pais, tamanho_torneio=3):
    # método de seleção de pais por torneio
    torneio = random.sample(pais, tamanho_torneio)
    print ("pais", pais)
    pai = max(torneio, key=lambda ind: ind[0])  # Seleciona o indivíduo com maior aptidão
    return pai[1]  # Retorna apenas os genes do pai selecionado


def selecao_roleta(pais):
    # Seleciona 2 pais baseado nas regras da roleta

    def sortear(fitness_total, indice_a_ignorar=-1):  # 2 parametro garante que não vai selecionar o mesmo elemento
        # Monta roleta para realizar o sorteio
        roleta, acumulado, valor_sorteado = [], 0, random.random()

        if indice_a_ignorar != -1:  # Desconta do total, o valor que sera retirado da roleta
            fitness_total -= valores[0][indice_a_ignorar]

        for indice, i in enumerate(valores[0]):
            if indice_a_ignorar == indice:  # ignora o valor ja utilizado na roleta
                continue
            acumulado += i
            roleta.append(acumulado / fitness_total)
            if roleta[-1] >= valor_sorteado:
                return indice

    valores = list(zip(*pais))  # cria 2 listas com os valores fitness e os cromossomos
    fitness_total = sum(valores[0])

    indice_pai1 = sortear(fitness_total)
    indice_pai2 = sortear(fitness_total, indice_pai1)

    pai = valores[1][indice_pai1]
    mae = valores[1][indice_pai2]

    return pai, mae
