import numpy
import requests


class Criptomoedas:

    moedas = []
    ganhos = {}
    riscos = {}

    @staticmethod
    def buscar_moeda(moeda):
        url = "https://min-api.cryptocompare.com/data/histoday?fsym=" + moeda + "&tsym=USD&allData=true"
        r = requests.get(url)
        historico = r.json()['Data']

        return historico

    @staticmethod
    def buscar(dia):
        lista_moedas = ['BTC', 'XRP', 'ETH', 'EOS', 'BCH', 'LTC', 'BNB', 'XLM',
                        'ADA', 'TRX', 'HT', 'XMR', 'DASH', 'BTMX', 'BSV', 'IOT',
                        'ONT', 'NEO', 'ETC', 'BAT', 'XEM', 'ZEC', 'VET', 'ORBS',
                        'DOGE', 'BTG', 'ZRX', 'QKC', 'QTUM', 'OMG', 'IOST', 'REP',
                        'WAVES', 'KCS', 'NANO', 'ATOM', 'TCH', 'ZB']

        for moeda in lista_moedas:
            historico = Criptomoedas.buscar_moeda(moeda)

            idx_dia = next((index for (index, d) in enumerate(historico) if d["time"] == dia), None)

            if idx_dia is not None:
                dados_dia = historico[idx_dia]
                ganho = dados_dia['close'] - dados_dia['open']

                Criptomoedas.moedas.append(moeda)
                Criptomoedas.ganhos[moeda] = ganho

                ultimos_10_dias = historico[(idx_dia - 10): idx_dia]
                valores_10_dias = [(x['close'] - x['open']) for x in ultimos_10_dias]

                numpy_array = numpy.array(valores_10_dias)
                Criptomoedas.riscos[moeda] = numpy_array.std()
