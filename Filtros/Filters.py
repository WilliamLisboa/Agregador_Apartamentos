#!/bin/

import pandas as pd

def FiltrandoPorPreco(df, nome_coluna_preco, precoMin, precoMax):

    condicao_preco = (df[nome_coluna_preco] >= precoMin) & (df[nome_coluna_preco] <= precoMax)
    print(df[condicao_preco])
    return df[condicao_preco]

def FiltrandoPorBairros(df, nome_coluna_endereco, bairros):
    condicao_bairro = df[nome_coluna_endereco].apply(lambda text:text.lower() in bairros)
    print(df[condicao_bairro])
    return df[condicao_bairro]
