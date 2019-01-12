import os
from urllib.request import urlretrieve
from zipfile import ZipFile

from toolbox import (xml_df_internal, save_files)

URL = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/documento_autor.zip'
arquivo = 'autores_proposicoes'
data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def get():
    urlretrieve(URL, 'data/documento_autor.zip')
    zip_file = ZipFile('data/documento_autor.zip', 'r')
    zip_file.extractall('data')
    zip_file.close()
    os.remove('data/documento_autor.zip')


def process_request():
    xml_data = 'data/documento_autor.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[['IdAutor', 'IdDocumento', 'NomeAutor']]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_proposicao',
        'IdAutor': 'id_autor',
        'NomeAutor': 'nome_autor'
    })
    save_files(dataset, data_dir, arquivo)
    os.remove(xml_data)


if __name__ == '__main__':
    create_dir()
    get()
    process_request()
