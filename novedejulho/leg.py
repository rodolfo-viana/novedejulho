import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)
from ndj_toolbox.format import remove_break_line

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'legislacao/legislacao_normas.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    urlretrieve(url, f'{DATA_DIR}/legislacao_normas.zip')
    zip_file = ZipFile(f'{DATA_DIR}/legislacao_normas.zip', 'r')
    zip_file.extractall(f'{DATA_DIR}')
    zip_file.close()
    os.remove(f'{DATA_DIR}/legislacao_normas.zip')

    xml_data = f'{DATA_DIR}/legislacao_normas.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'IdNorma', 'Numero', 'Ano', 'IdTipo', 'Data', 'Situacao', 'Ementa',
        'Autores', 'CadDO', 'PagDO', 'DataDO', 'URLDO', 'URLFicha',
        'URLIntegra', 'URLCompilado', 'Promulg', 'Ambito'
    ]]
    dataset = dataset.rename(columns={
        'IdNorma': 'id_norma',
        'Numero': 'nr_norma',
        'Ano': 'tx_ano',
        'IdTipo': 'id_tp_norma',
        'Data': 'dt_norma',
        'Situacao': 'tx_situacao',
        'Ementa': 'tx_ementa',
        'Autores': 'tx_autores',
        'CadDO': 'nr_caderno_do',
        'PagDO': 'nr_pagina_do',
        'DataDO': 'dt_publicacao_do',
        'URLDO': 'url_do',
        'URLFicha': 'url_ficha',
        'URLIntegra': 'url_integra',
        'URLCompilado': 'url_compilado',
        'Promulg': 'tx_promulg',
        'Ambito': 'tx_ambito'
    })

    dataset['tx_ementa'] = dataset['tx_ementa'].apply(remove_break_line)

    save_files(dataset, 'legislacao_normas')
    os.remove(xml_data)


if __name__ == '__main__':
    main()
