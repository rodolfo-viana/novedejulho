import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/proposituras.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    urlretrieve(url, f'{DATA_DIR}/proposituras.zip')
    zip_file = ZipFile(f'{DATA_DIR}/proposituras.zip', 'r')
    zip_file.extractall(f'{DATA_DIR}')
    zip_file.close()
    os.remove(f'{DATA_DIR}/proposituras.zip')

    xml_data = f'{DATA_DIR}/proposituras.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'AnoLegislativo', 'CodOriginalidade', 'Ementa', 'DtEntradaSistema',
        'DtPublicacao', 'IdDocumento', 'IdNatureza', 'NroLegislativo'
    ]]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_proposicao', 'CodOriginalidade': 'cd_originalidade',
        'AnoLegislativo': 'ano_legislativo',
        'DtEntradaSistema': 'dt_apresentacao', 'DtPublicacao': 'dt_publicacao',
        'IdNatureza': 'id_natureza', 'NroLegislativo': 'nr_legislativo',
        'Ementa': 'tx_ementa'
    })
    save_files(dataset, 'proposicoes')
    os.remove(xml_data)


if __name__ == '__main__':
    main()
