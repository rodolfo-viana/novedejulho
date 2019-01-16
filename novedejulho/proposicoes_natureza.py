import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url = 'https://www.al.sp.gov.br/repositorioDados/processo_legislativo/naturezasSpl.xml'
arquivo = 'proposicoes_natureza'
data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def process_request():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['idNatureza', 'nmNatureza', 'sgNatureza', 'tpNatureza']]
    dataset = dataset.rename(columns={
        'idNatureza': 'id_natureza', 'nmNatureza': 'nm_natureza',
        'sgNatureza': 'sg_natureza', 'tpNatureza': 'tp_natureza'
    })
    save_files(dataset, data_dir, arquivo)


if __name__ == '__main__':
    create_dir()
    process_request()
