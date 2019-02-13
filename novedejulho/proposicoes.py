import os
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/proposituras.zip'
url = url_base + url_file


def fetch_data():
    urlretrieve(url, 'data/proposituras.zip')
    zip_file = ZipFile('data/proposituras.zip', 'r')
    zip_file.extractall('data')
    zip_file.close()
    os.remove('data/proposituras.zip')


def process_proposicoes():
    xml_data = 'data/proposituras.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'AnoLegislativo', 'CodOriginalidade', 'Ementa', 'DtEntradaSistema',
        'DtPublicacao', 'IdDocumento', 'IdNatureza', 'NroLegislativo'
    ]]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_proposicao', 'CodOriginalidade': 'cd_originalidade',
        'AnoLegislativo': 'ano_legislativo',
        'DtEntradaSistema': 'dt_apresentacao', 'DtPublicacao': 'dt_publicacao',
        'IdNatureza': 'natureza', 'NroLegislativo': 'nr_legislativo',
        'Ementa': 'ementa'
    })
    save_files(dataset, 'data', 'proposicoes')
    os.remove(xml_data)


def main():
    fetch_data()
    process_proposicoes()


if __name__ == '__main__':
    main()
