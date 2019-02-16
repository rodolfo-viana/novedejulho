import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'administracao/funcionarios_cargos.xml'
url = url_base + url_file


def process_servidores_cargos():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'NomeFuncionario', 'NomeCargo', 'IdCargo', 'NomeRegime',
        'IdRegime', 'DataInicio', 'DataFim'
    ]]
    dataset = dataset.rename(columns={
        'NomeFuncionario': 'nm_funcionario', 'NomeCargo': 'nm_cargo',
        'IdCargo': 'id_cargo', 'NomeRegime': 'nm_regime',
        'IdRegime': 'id_regime', 'DataInicio': 'dt_inicio',
        'DataFim': 'dt_fim'
    })
    save_files(dataset, 'data', 'servidores_cargos')


def main():
    process_servidores_cargos()


if __name__ == '__main__':
    main()
