# This is a sample Python script.
from pandas import DataFrame

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import Generator
import Filters

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lista_apartamentos = Generator.requisicao_buscador()
    lista_apartamentos_filtrado = Filters.FiltrandoPorPreco(lista_apartamentos, "PRECO", 200000, 400000)
    bairros = ['móoca', 'mooca', 'bela vista', 'vila clementino', 'penha', 'pinheiros', 'bosque da saúde', 'saúde',
               'morumbi', 'tatuapé', 'vila mariana', 'vila olímpia', 'consolação', 'paraíso', 'perdizes',
               'malota', 'caxambu', 'vila arens', 'anhangabaú', 'parque da represa', 'parque residencial eloy chaves']
    lista_apartamentos_filtrado = Filters.FiltrandoPorBairros(lista_apartamentos_filtrado, 'BAIRRO', bairros)
    print(lista_apartamentos_filtrado.head())
    lista_apartamentos_filtrado.to_csv('./lista_apartamentos_filtrados.csv')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
