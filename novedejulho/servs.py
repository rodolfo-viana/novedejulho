import os
import csv
from datetime import datetime
import requests as req

from bs4 import BeautifulSoup
import pandas as pd

from ndj_toolbox.fetch import (ParseXmlRemote, save)
from ndj_toolbox.format import sanitize_float

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
DATA_DIR = f'data_{TODAY}'

cols_servs = {
    'NomeFuncionario': 'nm_funcionario',
    'NomeCargo': 'nm_cargo',
    'IdCargo': 'id_cargo',
    'NomeRegime': 'nm_regime',
    'IdRegime': 'id_regime',
    'DataInicio': 'dt_inicio',
    'DataFim': 'dt_fim'
}

cols_lot_atual = {
    'NomeFuncionario': 'nm_funcionario',
    'NomeCargo': 'nm_cargo',
    'IdCargo': 'id_cargo',
    'NomeRegime': 'nm_regime',
    'IdRegime': 'id_regime',
    'NomeUA': 'nm_unid_admin',
    'IdUA': 'id_unid_admin'
}

cols_lot_hist = {
    'NomeFuncionario': 'nm_funcionario',
    'NomeUA': 'nm_unid_admin',
    'IdUA': 'id_unid_admin',
    'DataInicio': 'dt_inicio',
    'DataFim': 'dt_fim'
}

cols_salarios = [
    'nm_funcionario', 'ano', 'mes', 'vlr_bruto', 'vlr_liquido', 'tributos',
    'abono_permanencia', 'ferias_bruto', 'ferias_liquido',
    'ferias_desconto', '13_bruto', '13_liquido', '13_desconto',
    'retroativo_bruto', 'retroativo_liquido', 'retroativo_desconto',
    'outros_bruto', 'outros_desconto', 'indenizacao'
]


def servs():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/administracao/'
    url_file = 'funcionarios_cargos.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'NomeFuncionario', 'NomeCargo', 'IdCargo', 'NomeRegime',
        'IdRegime', 'DataInicio', 'DataFim'
    ]]
    dataset = dataset.rename(columns=cols_servs)
    save(dataset, 'serv')


def lotacao_atual():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/administracao/'
    url_file = 'lotacoes.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'NomeFuncionario', 'NomeCargo', 'IdCargo',
        'NomeRegime', 'IdRegime', 'NomeUA', 'IdUA'
    ]]
    dataset = dataset.rename(columns=cols_lot_atual)
    save(dataset, 'serv_lotacao_atual')


def lotacao_historico():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/administracao/'
    url_file = 'funcionarios_lotacoes.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'NomeFuncionario', 'NomeUA', 'IdUA', 'DataInicio', 'DataFim'
    ]]
    dataset = dataset.rename(columns=cols_lot_hist)
    save(dataset, 'serv_lotacao_historico')


def salarios():
    with open('temp.csv', 'a') as file:
        dw = csv.DictWriter(file,
                            fieldnames=cols_salarios,
                            lineterminator='\n')
        dw.writeheader()
        ano_atual = datetime.now().year
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
                    dw.writerow({'nm_funcionario': tds[0].get_text().strip(),
                                 'ano': int(ano),
                                 'mes': int(mes),
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
                                 })

    dataset = pd.read_csv('temp.csv')
    save(dataset, 'serv_salarios')
    os.remove('temp.csv')


def main():
    servs()
    lotacao_atual()
    lotacao_historico()
    salarios()


if __name__ == '__main__':
    main()
