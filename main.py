from algoritmo_genetico.populacao import Populacao
from criptomoedas import Criptomoedas

if __name__ == '__main__':
    Criptomoedas.buscar(1561420800)
    ga = Populacao(tamanho_populacao=10, geracoes=5, valor_investimento=1000)
    ga.executar()
