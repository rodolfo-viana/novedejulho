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

    urlretrieve(url, f'{DATA_DIR}/documento_regime.zip')
    zip_file = ZipFile(f'{DATA_DIR}/documento_regime.zip', 'r')
    zip_file.extractall(f'{DATA_DIR}')
    zip_file.close()
    os.remove(f'{DATA_DIR}/documento_regime.zip')

    xml_data = f'{DATA_DIR}/documento_regime.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'IdDocumento', 'IdRegime', 'NomeRegime', 'DataInicio', 'DataFim'
    ]]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_documento',
        'IdRegime': 'id_regime',
        'NomeRegime': 'nm_regime',
        'DataInicio': 'dt_inicio',
        'DataFim': 'dt_fim'
    })

    save_files(dataset, 'documentos_regimes_tramitacao')
    os.remove(xml_data)


if __name__ == '__main__':
    main()
