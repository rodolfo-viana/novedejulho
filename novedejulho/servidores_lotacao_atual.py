import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url = 'http://www.al.sp.gov.br/repositorioDados/administracao/lotacoes.xml'
arquivo = 'servidores_lotacao_atual'
data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def process_request():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['NomeFuncionario', 'NomeCargo', 'IdCargo', 'NomeRegime',
                       'IdRegime', 'NomeUA', 'IdUA']]
    dataset = dataset.rename(columns={
        'NomeFuncionario': 'nm_funcionario', 'NomeCargo': 'nm_cargo',
        'IdCargo': 'id_cargo', 'NomeRegime': 'nm_regime',
        'IdRegime': 'id_regime', 'NomeUA': 'nm_unid_admin',
        'IdUA': 'id_unid_admin'
    })
    save_files(dataset, data_dir, arquivo)


if __name__ == '__main__':
    create_dir()
    process_request()
