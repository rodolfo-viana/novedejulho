import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'administracao/lotacoes.xml'
url = url_base + url_file


def process_servidores_lotacao_atual():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'NomeFuncionario', 'NomeCargo', 'IdCargo', 'NomeRegime',
        'IdRegime', 'NomeUA', 'IdUA'
    ]]
    dataset = dataset.rename(columns={
        'NomeFuncionario': 'nm_funcionario', 'NomeCargo': 'nm_cargo',
        'IdCargo': 'id_cargo', 'NomeRegime': 'nm_regime',
        'IdRegime': 'id_regime', 'NomeUA': 'nm_unid_admin',
        'IdUA': 'id_unid_admin'
    })
    save_files(dataset, 'data', 'servidores_lotacao_atual')


if __name__ == '__main__':
    process_servidores_lotacao_atual()
