import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)
from ndj_toolbox.format import remove_break_line

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'legislacao/legislacao_norma_anotacoes.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    urlretrieve(url, f'{DATA_DIR}/legislacao_norma_anotacoes.zip')
    zip_file = ZipFile(f'{DATA_DIR}/legislacao_norma_anotacoes.zip', 'r')
    zip_file.extractall(f'{DATA_DIR}')
    zip_file.close()
    os.remove(f'{DATA_DIR}/legislacao_norma_anotacoes.zip')

    xml_data = f'{DATA_DIR}/legislacao_norma_anotacoes.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'IdNorma', 'NumNormaRel', 'DataNormaRel', 'TipoNormaRel', 'DsRel',
        'DsOrigem', 'IdTipoRel', 'NumComplNormaRel'
    ]]
    dataset = dataset.rename(columns={
        'IdNorma': 'id_norma',
        'NumNormaRel': 'nr_norma_relacionada',
        'DataNormaRel': 'dt_norma_relacionada',
        'TipoNormaRel': 'tp_norma_relacionada',
        'DsRel': 'ds_anotacao',
        'DsOrigem': 'ds_origem',
        'IdTipoRel': 'id_tp_relacionada',
        'NumComplNormaRel': 'nr_complemento_norma_relacionada'
    })
    dataset['ds_anotacao'] = dataset['ds_anotacao'].apply(remove_break_line)

    save_files(dataset, 'legislacao_anotacoes')
    os.remove(xml_data)


if __name__ == '__main__':
    main()
