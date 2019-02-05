import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'deputados/deputados.xml'
url = url_base + url_file


def process_deputados():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'NomeParlamentar', 'Matricula', 'IdDeputado', 'IdSPL', 'IdUA',
        'Partido', 'Sala', 'Andar', 'Telefone', 'Email', 'PlacaVeiculo',
        'Aniversario', 'Situacao'
    ]]
    dataset = dataset.rename(columns={
        'NomeParlamentar': 'nm_deputado', 'Matricula': 'nr_matricula',
        'IdDeputado': 'id_deputado', 'IdSPL': 'id_spl',
        'IdUA': 'id_unid_admin', 'Partido': 'sg_partido', 'Sala': 'sala',
        'Andar': 'andar', 'Telefone': 'telefone', 'Email': 'email',
        'PlacaVeiculo': 'placa_carro', 'Aniversario': 'aniversario',
        'Situacao': 'status'
    })
    save_files(dataset, 'data', 'deputados')


if __name__ == '__main__':
    process_deputados()
