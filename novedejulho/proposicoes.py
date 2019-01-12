import os
from urllib.request import urlretrieve
from zipfile import ZipFile

from toolbox import (xml_df_internal, save_files)

URL = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/proposituras.zip'
arquivo = 'proposicoes'
data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def get():
    urlretrieve(URL, 'data/proposituras.zip')
    zip_file = ZipFile('data/proposituras.zip', 'r')
    zip_file.extractall('data')
    zip_file.close()
    os.remove('data/proposituras.zip')


def process_request():
    xml_data = 'data/proposituras.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[['AnoLegislativo', 'CodOriginalidade', 'Ementa',
                       'DtEntradaSistema', 'DtPublicacao', 'IdDocumento',
                       'IdNatureza', 'NroLegislativo']]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id', 'CodOriginalidade': 'cod_originalidade',
        'AnoLegislativo': 'ano_legislativo',
        'DtEntradaSistema': 'dt_apresentacao', 'DtPublicacao': 'dt_publicacao',
        'IdNatureza': 'natureza', 'NroLegislativo': 'nr_legislativo',
        'Ementa': 'ementa'
    })
    save_files(dataset, data_dir, arquivo)
    os.remove(xml_data)


if __name__ == '__main__':
    create_dir()
    get()
    process_request()
