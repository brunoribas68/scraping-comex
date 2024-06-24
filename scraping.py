# -*- coding: utf-8 -*-
import argparse
import sys

import requests
from bs4 import BeautifulSoup
import numpy as np
import json



def find_currency(data, currency_code):
    # Find the index of the row that matches the currency code
    mask = [row['code'] in currency_code for row in data]

    # Filtrando os dados usando a máscara
    filtered_data = data[mask]

    if len(filtered_data) > 0:
        return label_currency_data(filtered_data)
    else:
        return "Currency not found."

def find_number(data, currency_code):
    # Find the index of the row that matches the currency code
    mask = [row['number'] in currency_code for row in data]

    # Filtrando os dados usando a máscara
    filtered_data = data[mask]

    if len(filtered_data) > 0:
        return label_currency_data(filtered_data)
    else:
        return "Currency not found."


def label_currency_data(data):
    keys = ["code", "number", "decimal", "currency", "currency_location"]
    return dict(zip(keys, data))


def extract_currency_data():
    # URL da página da Wikipédia
    url = "https://pt.wikipedia.org/wiki/ISO_4217"

    # Realiza a solicitação HTTP
    response = requests.get(url)
    response.raise_for_status()  # Levanta um erro se a solicitação falhar

    # Analisa o conteúdo HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra a tabela com as informações de moedas
    table = soup.find('table', {'class': 'wikitable sortable'})

    # Inicializa a lista para armazenar os dados das moedas
    currencies = []

    # Itera pelas linhas da tabela
    for row in table.find_all('tr')[1:]:  # Pula o cabeçalho da tabela
        cols = row.find_all('td')
        if len(cols) > 0:
            code = cols[0].text.strip()
            number = cols[1].text if cols[1].text != "" else "None"
            decimal = cols[2].text
            currency = cols[3].text.strip()

            # Inicializa a lista de localizações para cada moeda
            currency_locations = []

            # Itera pelas colunas de países (exceto a primeira que contém o código do país)
            for col in cols[4:]:
                location_info = col.find('span', {'class': 'flagicon'})

                if location_info:
                    location = location_info.find_next_sibling()
                    location = location.next_element
                    icon = location_info.find('img')['src']

                else:
                    location = None
                    icon = ""

                currency_locations.append({
                    "location": location,
                    "icon": icon
                })

            # Adiciona as informações da moeda à lista
            currencies.append({
                "code": code,
                "number": number,
                "decimal": decimal,
                "currency": currency,
                "currency_locations": currency_locations
            })

    return np.array(currencies)
    # Salva os dados em um arquivo JSON
    # with open('currencies.json', 'w', encoding='utf-8') as f:
    #     json.dump(currencies, f, ensure_ascii=False, indent=4)
    #
    # # Exibe os dados coletados
    # print(json.dumps(currencies, ensure_ascii=False, indent=4))




def main(arg, arg_name):
    # Extrair dados

    argparse.ArgumentParser(description='Processar dados de moedas.')
    arg = arg.split(',')
    arg = np.array(arg)
    json_data = np.empty(0)
    coin_data = extract_currency_data()

    for currency in arg:
        if arg_name == 'coin':
            json_data = np.append(json_data, find_currency(coin_data, currency))
        else:
            json_data = np.append(json_data, find_number(coin_data, currency))

    return json_data



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processar dados de moedas.')


    # Adicionando o argumento --coin
    parser.add_argument('--coin', type=str, required=False, help='O código da moeda para processar')
    parser.add_argument('--number', type=str, required=False, help='O numero da moeda para processar')

    args = parser.parse_args()
    # Chamando a função principal com o argumento coin
    if args.coin:
        data = main(args.coin, 'coin')
    else:
        data = main(args.number, 'number')

    # Parseando os argumentos da linha de comando
    data_list = data.tolist()
    data_json = json.dumps(data_list)

    print(data_json)
    sys.exit()




