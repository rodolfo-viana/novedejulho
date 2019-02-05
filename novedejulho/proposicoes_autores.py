import os
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/documento_autor.zip'
url = url_base + url_file


def fetch_data():
    urlretrieve(url, 'data/documento_autor.zip')
    zip_file = ZipFile('data/documento_autor.zip', 'r')
    zip_file.extractall('data')
    zip_file.close()
    os.remove('data/documento_autor.zip')


def process_proposicoes_autores():
    xml_data = 'data/documento_autor.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[['IdAutor', 'IdDocumento', 'NomeAutor']]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_proposicao',
        'IdAutor': 'id_autor',
        'NomeAutor': 'nm_autor'
    })
    save_files(dataset, 'data', 'proposicoes_autores')
    os.remove(xml_data)


if __name__ == '__main__':
    fetch_data()
    process_proposicoes_autores()
