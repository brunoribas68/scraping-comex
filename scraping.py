import argparse
import sys

import requests
from bs4 import BeautifulSoup
import numpy as np

def find_currency(data, currency_code):
    # Find the index of the row that matches the currency code
    index = np.where(data[:, 0] == currency_code)[0]

    if len(index) > 0:
        return label_currence_data(data[index[0]])
    else:
        return "Currency not found."

def label_currence_data(data):
    keys = ["ISO", "numero", "casa_decimal", "moeda", "pais"]
    return dict(zip(keys, data))

def getCoinData(coin):
    # URL do artigo da Wikipedia que contém a tabela
    url = "https://pt.wikipedia.org/wiki/ISO_4217"

    # Enviar uma solicitação HTTP GET para a URL
    response = requests.get(url)
    # Verificar se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Analisar o conteúdo HTML da página
        soup = BeautifulSoup(response.content, "html.parser")

        # Encontrar a tabela com a classe 'wikitable sortable jquery-tablesorter'
        table = soup.find("table", {"class": "wikitable"})
        # print(table)
        # sys.exit()
        if table:
            # Inicializar uma lista para armazenar os dados da tabela
            table_data = []

            # Iterar sobre as linhas da tabela
            for row in table.find_all("tr"):
                # Encontrar todas as células (td) e cabeçalhos (th) da linha
                cells = row.find_all(["td", "th"])

                # Extrair o texto de cada célula e armazenar em uma lista
                cell_data = [cell.get_text(strip=True) for cell in cells]

                # Adicionar os dados da linha à lista de dados da tabela
                table_data.append(cell_data)
            data_to_np = np.array(table_data)

            print(find_currency(data_to_np, coin))
            sys.exit()

        else:
            print("Tabela não encontrada.")
    else:
        print("Falha ao acessar a página da Wikipedia.")

def main(coin = 'GBP'):
    parser = argparse.ArgumentParser(description='Processar dados de moedas.')

    coin_data = getCoinData(coin)
    coin_data = find_currency(coin_data)
    np.savetxt("coin_data.csv", np.asarray(coin_data), delimiter=",")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processar dados de moedas.')

    # Adicionando o argumento --coin
    parser.add_argument('--coin', type=str, required=True, help='O código da moeda para processar')

    # Parseando os argumentos da linha de comando
    args = parser.parse_args()

    # Chamando a função principal com o argumento coin
    main(args.coin)