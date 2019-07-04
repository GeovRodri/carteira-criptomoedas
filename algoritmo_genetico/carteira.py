import random
from random import randint
from criptomoedas import Criptomoedas


class Carteira:

    def __init__(self, tamanho, pesos=None):
        self.tamanho = tamanho
        self.moedas = []
        self.avaliacao = -1
        self.pesos = pesos

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
        novo_valor = []

        for i in range(self.tamanho):
            if i%2 == 0:
                if self.moedas[i] not in novo_valor:
                    novo_valor.append(self.moedas[i])
                else:
                    novo_valor.append(outro_cromossomo.moedas[i])
            else:
                if outro_cromossomo.moedas[i] not in novo_valor:
                    novo_valor.append(outro_cromossomo.moedas[i])
                else:
                    novo_valor.append(self.moedas[i])

        novo_cromossomo = Carteira(self.tamanho)
        novo_cromossomo.set_valor(novo_valor)
        novo_cromossomo.set_pesos(self.pesos)
        return novo_cromossomo

    def mutacao(self, chance_mutacao):
        for i in range(self.tamanho):
            if random.random() < chance_mutacao:
                self.moedas[i] = self.gerar_moeda_aleatoria()

    def avaliar(self):
        x = self.get_ganho_carteira(True)
        self.avaliacao = x
        return self.avaliacao

    def __repr__(self):
        return "cromossomo:[%s] pesos:[%s] avaliacao[%.2f] valor ganho [%.4f]" \
               % (self.moedas, self.pesos, self.avaliacao, self.get_ganho_carteira())
