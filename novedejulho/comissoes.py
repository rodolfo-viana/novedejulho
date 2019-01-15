import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url = 'https://www.al.sp.gov.br/repositorioDados/processo_legislativo/comissoes.xml'
arquivo = 'comissoes'
data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def process_request():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['IdComissao', 'NomeComissao', 'SiglaComissao',
                       'DescricaoComissao', 'DataFimComissao']]
    dataset = dataset.rename(columns={
        'IdComissao': 'id_comissao', 'NomeComissao': 'nm_comissao',
        'SiglaComissao': 'sg_comissao', 'DescricaoComissao': 'ds_comissao',
        'DataFimComissao': 'dt_fim_comissao',
    })
    save_files(dataset, data_dir, arquivo)


if __name__ == '__main__':
    create_dir()
    process_request()
