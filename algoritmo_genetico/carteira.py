import math
import random
from random import randint
from criptomoedas import Criptomoedas


class Carteira:

    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.moedas = []
        self.avaliacao = -1

    def set_valor(self, novo_valor):
        self.moedas = novo_valor

    def gerar_moeda_aleatoria(self):
        quantidade = len(Criptomoedas.moedas)
        id_moeda = randint(0, (quantidade - 1))

        while Criptomoedas.moedas[id_moeda] in self.moedas:
            id_moeda = randint(0, (quantidade - 1))

        return Criptomoedas.moedas[id_moeda]

    def get_ganho_carteira(self, calcular_desvio=False):
        valor = 0
        
        for moeda in self.moedas:
            valor += Criptomoedas.ganhos[moeda]

            if calcular_desvio is True:
                valor -= Criptomoedas.dps[moeda]

        return valor

    def inicializar(self):
        for i in range(self.tamanho):
            moeda = self.gerar_moeda_aleatoria()
            self.moedas.append(moeda)

    def crossover(self, outro_cromossomo):
        split_index = int(random.random() * self.tamanho)

        if random.random() > .5:
            novo_valor = self.moedas[0:split_index] + outro_cromossomo.moedas[split_index:len(outro_cromossomo.moedas)]
        else:
            novo_valor = outro_cromossomo.moedas[0:split_index] + self.moedas[split_index:len(outro_cromossomo.moedas)]

        novo_cromossomo = Carteira(self.tamanho)
        novo_cromossomo.set_valor(novo_valor)
        return novo_cromossomo

    def mutacao(self, chance_mutacao):
        for i in range(self.tamanho):
            if random.random() < chance_mutacao:
                inicio = self.moedas[0:i]
                fim = self.moedas[i + 1: self.tamanho]
                nova = self.gerar_moeda_aleatoria()

                self.set_valor(inicio + [nova] + fim)

    def avaliar(self):
        x = self.get_ganho_carteira(False)
        self.avaliacao = math.sin(x ** 2) / (3 - math.cos(math.e) - x)
        return self.avaliacao

    def __repr__(self):
        return "cromossomo:[%s] avaliacao[%.2f] valor ganho [%.4f]" \
               % (self.moedas, self.avaliacao, self.get_ganho_carteira())
