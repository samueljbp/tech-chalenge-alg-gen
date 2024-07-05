import random


def individual(n_de_itens):
    """Cria um membro da populacao"""
    return [random.getrandbits(1) for x in range(n_de_itens)]


def population(n_de_individuos, n_de_itens):
    """"Cria a populacao"""
    return [individual(n_de_itens) for x in range(n_de_individuos)]


def reproduce(pais, tamanho_populacao, tecnica_selecao = "T", elitismo=True, melhor_individuo=[]):
    filhos = []

    if elitismo and melhor_individuo != []:
        print("Melhor ind", melhor_individuo)
        # Mantém o melhor indivíduo
        filhos.append(melhor_individuo)

    # torneio
    if tecnica_selecao == "T":
        tamanho_torneio = 10
        while len(filhos) < tamanho_populacao:
            pai1_genes = selecao_torneio(pais, tamanho_torneio)
            pai2_genes = selecao_torneio(pais, tamanho_torneio)
            meio = len(pai1_genes) // 2
            filho_genes = pai1_genes[:meio] + pai2_genes[meio:]
            filhos.append(filho_genes)
    
    # roleta
    if tecnica_selecao == "R":
        while len(filhos) < tamanho_populacao:
            # seleciona os pais por roleta
            pai1, pai2 = selecao_roleta(pais)

            # Cruzamento de Um Ponto
            meio = len(pai1) // 2
            filho = pai1[:meio] + pai2[meio:]
            filhos.append(filho)

    return filhos

def selecao_torneio(pais, tamanho_torneio=3):
    torneio = random.sample(pais, tamanho_torneio)
    print ("pais", pais)
    pai = max(torneio, key=lambda ind: ind[0])  # Seleciona o indivíduo com maior aptidão
    return pai[1]  # Retorna apenas os genes do pai selecionado


def mutate(mutation_probability, individuo):
    # técnica Mutação de Bit
    if mutation_probability > random.random():
        pos_to_mutate = random.randint(0, len(individuo) - 1)
        if individuo[pos_to_mutate] == 1:
            individuo[pos_to_mutate] = 0
        else:
            individuo[pos_to_mutate] = 1

    return individuo


def fitness(individuo, peso_maximo, pesos_e_valores):
    """Faz avaliacao do individuo"""
    peso_total, valor_total = 0, 0
    for indice, valor in enumerate(individuo):
        peso_total += (individuo[indice] * pesos_e_valores[indice][0])
        valor_total += (individuo[indice] * pesos_e_valores[indice][1])

    if (peso_maximo - peso_total) < 0:
        return -1  # retorna -1 no caso de peso excedido
    return valor_total  # se for um individuo valido retorna seu valor, sendo maior melhor


def media_fitness(populacao, peso_maximo,
                  pesos_e_valores):  # só leva em consideracao os elementos que respeitem o peso maximo da mochila
    """Encontra a avalicao media da populacao"""
    summed = sum(
        fitness(x, peso_maximo, pesos_e_valores) for x in populacao if fitness(x, peso_maximo, pesos_e_valores) >= 0)
    return summed / (len(populacao) * 1.0)


def melhor_solucao(populacao, peso_maximo,
                   pesos_e_valores):  # só leva em consideracao os elementos que respeitem o peso maximo da mochila
    """Encontra a avalicao media da populacao"""
    melhor_fit = 0
    melhor_sol = ()
    for x in populacao:
        fit = fitness(x, peso_maximo, pesos_e_valores)
        if fit > melhor_fit:
            melhor_fit = fit
            melhor_sol = x

    return melhor_fit, melhor_sol

def selecao_roleta(pais):
    """Seleciona um pai e uma mae baseado nas regras da roleta"""

    def sortear(fitness_total, indice_a_ignorar=-1):  # 2 parametro garante que não vai selecionar o mesmo elemento (
        # elitismo)
        """Monta roleta para realizar o sorteio"""
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

    indice_pai = sortear(fitness_total)
    indice_mae = sortear(fitness_total, indice_pai)

    pai = valores[1][indice_pai]
    mae = valores[1][indice_mae]

    return pai, mae
