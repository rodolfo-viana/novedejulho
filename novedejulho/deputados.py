import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url = 'https://www.al.sp.gov.br/repositorioDados/deputados/deputados.xml'
arquivo = 'deputados'
data_dir = 'data/'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def process_request():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['NomeParlamentar', 'Matricula', 'IdDeputado',
                       'IdSPL', 'IdUA', 'Partido', 'Sala', 'Andar',
                       'Telefone', 'Email', 'PlacaVeiculo',
                       'Aniversario', 'Situacao']]
    dataset = dataset.rename(columns={
        'NomeParlamentar': 'nome', 'Matricula': 'matricula',
        'IdDeputado': 'id', 'IdSPL': 'id_spl', 'IdUA': 'id_unid_admin',
        'Partido': 'partido', 'Sala': 'sala', 'Andar': 'andar',
        'Telefone': 'telefone', 'Email': 'email',
        'PlacaVeiculo': 'placa_carro', 'Aniversario': 'aniversario',
        'Situacao': 'status'
    })
    save_files(dataset, data_dir, arquivo)


if __name__ == '__main__':
    print(f'Criando e acessando a pasta {data_dir}...')
    create_dir()
    print('Baixando e formatando os dados...')
    process_request()
    print(f'Finalizado!\nDados salvos nos arquivos {arquivo}.csv e {arquivo}.xz.')
