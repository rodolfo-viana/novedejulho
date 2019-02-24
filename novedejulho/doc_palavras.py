import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/documento_palavras.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    urlretrieve(url, f'{DATA_DIR}/documento_palavras.zip')
    zip_file = ZipFile(f'{DATA_DIR}/documento_palavras.zip', 'r')
    zip_file.extractall(f'{DATA_DIR}')
    zip_file.close()
    os.remove(f'{DATA_DIR}/documento_palavras.zip')

    xml_data = f'{DATA_DIR}/documento_palavras.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[['IdDocumento', 'IdPalavra']]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_documento',
        'IdPalavra': 'id_palavra'
    })
    save_files(dataset, 'documentos_palavras')
    os.remove(xml_data)


if __name__ == '__main__':
    main()
