import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/documento_regime.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'
    file_path = os.path.join(DATA_DIR, 'documento_regime.zip')

    urlretrieve(url, file_path)
    zip_file = ZipFile(file_path, 'r')
    zip_file.extractall(DATA_DIR)
    zip_file.close()
    os.remove(file_path)

    xml_data = os.path.join(DATA_DIR, 'documento_regime.xml')
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'IdDocumento', 'IdRegime', 'NomeRegime', 'DataInicio',
        'DataFim'
    ]]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_documento', 'IdRegime': 'id_regime',
        'NomeRegime': 'nm_regime', 'DataInicio': 'dt_inicio',
        'DataFim': 'dt_fim'
    })

    save_files(dataset, 'proposicoes_regime')
    os.remove(xml_data)


if __name__ == '__main__':
    main()
