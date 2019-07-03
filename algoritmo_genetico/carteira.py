import random
import numpy as np
from random import randint
from criptomoedas import Criptomoedas


class Carteira:

    def __init__(self, tamanho, valor_investimento=1000):
        self.tamanho = tamanho
        self.moedas = []
        self.avaliacao = -1
        self.pesos = self.gerar_pesos(valor_investimento, tamanho)

    def set_valor(self, novo_valor):
        self.moedas = novo_valor

    def set_pesos(self, novo_valor):
        self.pesos = novo_valor

    def gerar_moeda_aleatoria(self):
        quantidade = len(Criptomoedas.moedas)
        id_moeda = randint(0, (quantidade - 1))

        while Criptomoedas.moedas[id_moeda] in self.moedas:
            id_moeda = randint(0, (quantidade - 1))

        return Criptomoedas.moedas[id_moeda]

    def get_ganho_carteira(self, calcular_desvio=False):
        valor = 0
        
        for index, moeda in enumerate(self.moedas):
            valor += (Criptomoedas.ganhos[moeda] * self.pesos[index])

            if calcular_desvio is True:
                valor -= Criptomoedas.riscos[moeda]

        return valor

    def inicializar(self):
        for i in range(self.tamanho):
            moeda = self.gerar_moeda_aleatoria()
            self.moedas.append(moeda)

    def crossover(self, outro_cromossomo):
        split_index = int(random.random() * self.tamanho)

        if random.random() > .5:
            novo_valor = self.moedas[0:split_index] + outro_cromossomo.moedas[split_index:len(outro_cromossomo.moedas)]
            novo_peso = self.pesos[0:split_index] + outro_cromossomo.pesos[split_index:len(outro_cromossomo.pesos)]
        else:
            novo_valor = outro_cromossomo.moedas[0:split_index] + self.moedas[split_index:len(outro_cromossomo.moedas)]
            novo_peso = outro_cromossomo.pesos[0:split_index] + self.pesos[split_index:len(outro_cromossomo.pesos)]

        novo_cromossomo = Carteira(self.tamanho)
        novo_cromossomo.set_valor(novo_valor)
        novo_cromossomo.set_pesos(novo_peso)
        return novo_cromossomo

    def mutacao(self, chance_mutacao):
        for i in range(self.tamanho):
            if random.random() < chance_mutacao:
                self.moedas[i] = self.gerar_moeda_aleatoria()

    def avaliar(self):
        x = self.get_ganho_carteira(True)
        self.avaliacao = x
        return self.avaliacao

    def gerar_pesos(self, valor, tamanho):
        valor_maximo = valor
        peso_maximo = valor * 0.2
        pesos = np.zeros(tamanho)
        i = 0

        while i != tamanho:
            valor_aleatorio = randint(0, min(valor_maximo, peso_maximo))
            pesos[i] = valor_aleatorio

            if i == (tamanho - 1):
                pesos[i] = valor_maximo

            valor_maximo -= valor_aleatorio
            i += 1

        return pesos.tolist()

    def __repr__(self):
        return "cromossomo:[%s] pesos:[%s] avaliacao[%.2f] valor ganho [%.4f]" \
               % (self.moedas, self.pesos, self.avaliacao, self.get_ganho_carteira())
