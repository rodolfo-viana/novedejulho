import os
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
url_file = 'documento_palavras.zip'
url = url_base + url_file


def fetch_data():
    urlretrieve(url, 'data/documento_palavras.zip')
    zip_file = ZipFile('data/documento_palavras.zip', 'r')
    zip_file.extractall('data')
    zip_file.close()
    os.remove('data/documento_palavras.zip')


def process_proposicoes_palavras():
    xml_data = 'data/documento_palavras.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[['IdDocumento', 'IdPalavra']]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_proposicao', 'IdPalavra': 'id_palavra'
    })
    save_files(dataset, 'data', 'proposicoes_palavras')
    os.remove(xml_data)


if __name__ == '__main__':
    fetch_data()
    process_proposicoes_palavras()
