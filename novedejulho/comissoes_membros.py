import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url = 'https://www.al.sp.gov.br/repositorioDados/processo_legislativo/comissoes_membros.xml'
arquivo = 'comissoes_membros'
data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def process_request():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['SiglaComissao', 'IdComissao', 'NomeMembro',
                       'IdMembro', 'Papel', 'IdPapel', 'Efetivo',
                       'DataInicio', 'DataFim']]
    dataset = dataset.rename(columns={
        'SiglaComissao': 'sg_comissao', 'IdComissao': 'id_comissao',
        'NomeMembro': 'nm_membro', 'IdMembro': 'id_membro',
        'Papel': 'ds_papel', 'IdPapel': 'id_papel', 'Efetivo': 'efetivo',
        'DataInicio': 'dt_inicio', 'DataFim': 'dt_fim'
    })
    save_files(dataset, data_dir, arquivo)


if __name__ == '__main__':
    create_dir()
    process_request()
