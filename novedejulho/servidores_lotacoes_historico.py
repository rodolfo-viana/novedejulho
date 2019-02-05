import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'administracao/funcionarios_lotacoes.xml'
url = url_base + url_file


def process_servidores_lotacoes_historico():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'NomeFuncionario', 'NomeUA', 'IdUA', 'DataInicio', 'DataFim'
    ]]
    dataset = dataset.rename(columns={
        'NomeFuncionario': 'nm_funcionario', 'NomeUA': 'nm_unid_admin',
        'IdUA': 'id_unid_admin', 'DataInicio': 'dt_inicio', 'DataFim': 'dt_fim'
    })
    save_files(dataset, 'data', 'servidores_lotacoes_historico')


if __name__ == '__main__':
    process_servidores_lotacoes_historico()
