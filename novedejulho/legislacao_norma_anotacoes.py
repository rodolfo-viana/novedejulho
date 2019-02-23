import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'legislacao/legislacao_norma_anotacoes.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'
    file_path = os.path.join(DATA_DIR, 'legislacao_norma_anotacoes.zip')

    urlretrieve(url, file_path)
    zip_file = ZipFile(file_path, 'r')
    zip_file.extractall(DATA_DIR)
    zip_file.close()
    os.remove(file_path)

    xml_data = os.path.join(DATA_DIR, 'legislacao_norma_anotacoes.xml')
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'IdNorma', 'NumNormaRel', 'DataNormaRel', 'TipoNormaRel',
        'DsRel', 'DsOrigem', 'IdTipoRel', 'NumComplNormaRel'
    ]]
    dataset = dataset.rename(columns={
        'IdNorma': 'id_norma', 'NumNormaRel': 'nr_norma_rel',
        'DataNormaRel': 'dt_norma_rel', 'TipoNormaRel': 'tp_norma_rel',
        'DsRel': 'ds_rel', 'DsOrigem': 'ds_origem',
        'IdTipoRel': 'id_tp_rel', 'NumComplNormaRel': 'nr_compl_norma_rel'
    })
    dataset['ds_rel'] = dataset['ds_rel'].apply(remove_break_line)

    save_files(dataset, 'legislacao_norma_anotacoes')
    os.remove(xml_data)


def remove_break_line(text):
    try:
        return text.replace('\n', '')
    except:
        return text


if __name__ == '__main__':
    main()
