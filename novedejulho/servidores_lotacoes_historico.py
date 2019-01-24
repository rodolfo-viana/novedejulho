import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url = 'https://www.al.sp.gov.br/repositorioDados/administracao/funcionarios_lotacoes.xml'
arquivo = 'servidores_lotacoes_historico'
data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def process_request():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['NomeFuncionario', 'NomeUA', 'IdUA', 'DataInicio',
                       'DataFim']]
    dataset = dataset.rename(columns={
        'NomeFuncionario': 'nm_funcionario', 'NomeUA': 'nm_unid_admin',
        'IdUA': 'id_unid_admin', 'DataInicio': 'dt_inicio', 'DataFim': 'dt_fim'
    })
    save_files(dataset, data_dir, arquivo)


if __name__ == '__main__':
    create_dir()
    process_request()
