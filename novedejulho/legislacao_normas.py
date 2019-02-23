import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'legislacao/legislacao_normas.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'
    file_path = os.path.join(DATA_DIR, 'legislacao_normas.zip')

    urlretrieve(url, file_path)
    zip_file = ZipFile(file_path, 'r')
    zip_file.extractall(DATA_DIR)
    zip_file.close()
    os.remove(file_path)

    xml_data = os.path.join(DATA_DIR, 'legislacao_normas.xml')
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'IdNorma', 'Numero', 'Ano', 'IdTipo',
        'Data', 'Situacao', 'Ementa', 'Autores',
        'CadDO', 'PagDO', 'DataDO', 'URLDO',
        'URLFicha', 'URLIntegra', 'URLCompilado',
        'Promulg', 'Ambito'
    ]]
    dataset = dataset.rename(columns={
        'IdNorma': 'id_norma', 'Numero': 'nm', 'Ano': 'ano',
        'IdTipo': 'id_tp', 'Data': 'dt', 'Situacao': 'situacao',
        'Ementa': 'ementa', 'Autores': 'autores', 'CadDO': 'cad_do',
        'PagDO': 'pg_do', 'DataDO': 'dt_do', 'URLDO': 'url_do',
        'URLFicha': 'url_ficha', 'URLIntegra': 'url_integra', 'URLCompilado': 'url_compilado',
        'Promulg': 'promulg', 'Ambito': 'ambito'
    })

    dataset['ementa'] = dataset['ementa'].apply(remove_break_line)

    save_files(dataset, 'legislacao_normas')
    os.remove(xml_data)


def remove_break_line(text):
    try:
        return text.replace('\n', '')
    except:
        return text


if __name__ == '__main__':
    main()
