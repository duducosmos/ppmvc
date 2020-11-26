#!/usr/bin/env python
# -*- Coding: UTF-8 -*-
import pandas as pd
import requests
import requests_cache
from bs4 import BeautifulSoup
from numpy import array

from model import DB as db

requests_cache.install_cache('wikipedia_cache')


def coletar_limpar_dados():

    url = "https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_popula%C3%A7%C3%A3o"

    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(url, headers=header)

    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find('table')

    table = tables.get_text().split("\n")
    table = [ti for ti in table if ti != ""][6:]
    table = array([table[i: i + 5] for i in range(0, len(table), 5)])

    estados = array([ti.replace("\xa0", "") for ti in table[:, 1]])
    populacao = {estados[i]: int(table[:, 2][i].replace(" ", ""))
                 for i in range(table[:, 2].size)}
    return estados, populacao


def injetar_dados():

    estados, populacao = coletar_limpar_dados()

    UFS = {'São Paulo': "SP", 'Minas Gerais': "MG",
           'Rio de Janeiro': 'RJ',
           'Bahia': 'BA', 'Paraná': 'PA',
           'Rio Grande do Sul': 'RS', 'Pernambuco': 'PE',
           'Ceará': 'CE', 'Pará': 'PR',
           'Santa Catarina': 'SC', 'Goiás': 'GO',
           'Maranhão': 'MA', 'Amazonas': 'AM',
           'Espírito Santo': 'ES', 'Paraíba': 'PB',
           'Rio Grande do Norte': 'RN', 'Mato Grosso': 'MT',
           'Alagoas': 'AL',   'Piauí': 'PI',
           'Distrito Federal': 'DF', 'Mato Grosso do Sul': 'MS',
           'Sergipe': 'SE',  'Rondônia': 'RO', 'Tocantins': 'TO',
           'Acre': 'AC', 'Amapá': "AP", 'Roraima': "RR"}

    for es in estados:
        db.populacao_total.update_or_insert(
            (db.populacao_total.uf == UFS[es]),
            uf=UFS[es],
            populacao=populacao[es]
        )

        db.uf_nome.update_or_insert(
            (db.uf_nome.uf == UFS[es]),
            uf=UFS[es],
            nome=es
        )

    db.commit()


if __name__ == "__main__":
    injetar_dados()
