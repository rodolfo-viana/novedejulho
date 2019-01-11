import os
import datetime

import pandas as pd
from bs4 import BeautifulSoup
import requests as req
from novedejulho.toolbox import (save_files)

url_base = 'https://www.al.sp.gov.br/repositorio/folha-de-pagamento/'
arquivo_base = 'folha-{}-{}-detalhada.html'
arquivo = 'servidores_salarios'
data_dir = 'data/'
ano_atual = datetime.datetime.now().year


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def fetch_data():
    for ano in range(2016, ano_atual + 1):
        for mes in range(1, 13):
            lista = []
            url = url_base + arquivo_base.format(ano, mes)
            data = req.get(url).content
            soup = BeautifulSoup(data, 'html.parser')
            for tr in soup.find_all('tr')[1:]:
                col = 0
                for i in tr.find_all('td'):
                    td_limpo = i.get_text().strip()
                    td_nmr_limpo = i.get_text().strip().replace('.', '')\
                                                       .replace(',', '.')
                    if col == 0:
                        nome = td_limpo
                    if col == 1:
                        bruto = td_nmr_limpo
                    if col == 2:
                        liquido = td_nmr_limpo
                    if col == 3:
                        tributos = td_nmr_limpo
                    if col == 4:
                        abono_perm = td_nmr_limpo
                    if col == 5:
                        ferias_bruto = td_nmr_limpo
                    if col == 6:
                        ferias_desc = td_nmr_limpo
                    if col == 7:
                        ferias_liq = td_nmr_limpo
                    if col == 8:
                        bruto_13 = td_nmr_limpo
                    if col == 9:
                        desc_13 = td_nmr_limpo
                    if col == 10:
                        liq_13 = td_nmr_limpo
                    if col == 11:
                        retroativo_bruto = td_nmr_limpo
                    if col == 12:
                        retroativo_desc = td_nmr_limpo
                    if col == 13:
                        retroativo_liq = td_nmr_limpo
                    if col == 14:
                        outros_bruto = td_nmr_limpo
                    if col == 15:
                        outros_desc = td_nmr_limpo
                    if col == 16:
                        indenizacao = td_nmr_limpo
                        lista.append({'nome': nome,
                                      'ano': ano,
                                      'mes': mes,
                                      'vlr_bruto': float(bruto),
                                      'vlr_liquido': float(liquido),
                                      'tributos': float(tributos),
                                      'abono_permanencia': float(abono_perm),
                                      'ferias_bruto': float(ferias_bruto),
                                      'ferias_liquido': float(ferias_liq),
                                      'ferias_desconto': float(ferias_desc),
                                      '13_bruto': float(bruto_13),
                                      '13_liquido': float(liq_13),
                                      '13_desconto': float(desc_13),
                                      'retroativo_bruto': float(retroativo_bruto),
                                      'retroativo_liquido': float(retroativo_liq),
                                      'retroativo_desconto': float(retroativo_desc),
                                      'outros_bruto': float(outros_bruto),
                                      'outros_desconto': float(outros_desc),
                                      'indenizacao': float(indenizacao)})
                    col += 1
    df = pd.DataFrame(lista, columns=['nome', 'ano', 'mes', 'vlr_bruto',
                                      'vlr_liquido', 'tributos',
                                      'abono_permanencia', 'ferias_bruto',
                                      'ferias_liquido', 'ferias_desconto',
                                      '13_bruto', '13_liquido', '13_desconto',
                                      'retroativo_bruto', 'retroativo_liquido',
                                      'retroativo_desconto', 'outros_bruto',
                                      'outros_desconto', 'indenizacao'])
    save_files(df, data_dir, arquivo)


if __name__ == '__main__':
    create_dir()
    fetch_data()
