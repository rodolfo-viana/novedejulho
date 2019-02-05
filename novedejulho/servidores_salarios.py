import datetime

import pandas as pd
from bs4 import BeautifulSoup
import requests as req
from ndj_toolbox.fetch import (save_files)
from ndj_toolbox.format import (sanitize_float)

ano_atual = datetime.datetime.now().year

cols = [
    'nm_funcionario', 'ano', 'mes', 'vlr_bruto', 'vlr_liquido', 'tributos',
    'abono_permanencia', 'ferias_bruto', 'ferias_liquido', 'ferias_desconto',
    '13_bruto', '13_liquido', '13_desconto', 'retroativo_bruto',
    'retroativo_liquido', 'retroativo_desconto', 'outros_bruto',
    'outros_desconto', 'indenizacao'
]


def process_servidores_salarios():
    df = pd.DataFrame(columns=cols)
    for ano in range(2014, ano_atual + 1):
        for mes in range(1, 13):
            mes = format(mes, '02d')
            url_base = 'https://www.al.sp.gov.br/repositorio/'
            url_file = f'folha-de-pagamento/folha-{ano}-{mes}-detalhada.html'
            url = url_base + url_file
            data = req.get(url).content
            soup = BeautifulSoup(data, 'html.parser')
            for tr in soup.find_all('tr')[1:]:
                tds = tr.find_all('td')
                dicionario = {'nm_funcionario': tds[0].get_text().strip(),
                              'ano': ano,
                              'mes': mes,
                              'vlr_bruto': sanitize_float(tds[1]),
                              'vlr_liquido': sanitize_float(tds[2]),
                              'tributos': sanitize_float(tds[3]),
                              'abono_permanencia': sanitize_float(tds[4]),
                              'ferias_bruto': sanitize_float(tds[5]),
                              'ferias_desconto': sanitize_float(tds[6]),
                              'ferias_liquido': sanitize_float(tds[7]),
                              '13_bruto': sanitize_float(tds[8]),
                              '13_desconto': sanitize_float(tds[9]),
                              '13_liquido': sanitize_float(tds[10]),
                              'retroativo_bruto': sanitize_float(tds[11]),
                              'retroativo_desconto': sanitize_float(tds[12]),
                              'retroativo_liquido': sanitize_float(tds[13]),
                              'outros_bruto': sanitize_float(tds[14]),
                              'outros_desconto': sanitize_float(tds[15]),
                              'indenizacao': sanitize_float(tds[16])
                              }
                df = df.append(dicionario, ignore_index=True)
    save_files(df, 'data', 'servidores_salarios')


if __name__ == '__main__':
    process_servidores_salarios()
