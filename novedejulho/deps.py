import requests as req

from ndj_toolbox.fetch import (ParseXmlRemote, save)
from ndj_toolbox.format import clean_expenses_categories

cols_deps = {
    'NomeParlamentar': 'nm_deputado',
    'Matricula': 'nr_matricula',
    'IdDeputado': 'id_deputado',
    'IdSPL': 'id_spl',
    'IdUA': 'id_unid_admin',
    'Partido': 'sg_partido',
    'Sala': 'tx_sala',
    'Andar': 'tx_andar',
    'Telefone': 'tx_telefone',
    'Email': 'tx_email',
    'PlacaVeiculo': 'tx_placa_carro',
    'Aniversario': 'tx_aniversario',
    'Situacao': 'tx_status'
}

cols_area = {
    'IdDeputado': 'id_deputado',
    'IdArea': 'id_area',
    'NrOrdem': 'nr_ordem'
}

cols_base = {
    'IdDeputado': 'id_deputado',
    'IdBaseEleitoral': 'id_base',
    'NrOrdem': 'nr_ordem'
}

cols_gastos = {
    'Deputado': 'nm_deputado',
    'Matricula': 'nr_matricula',
    'Ano': 'nr_ano',
    'Mes': 'nr_mes',
    'Tipo': 'tp_categoria',
    'Fornecedor': 'nm_fornecedor',
    'CNPJ': 'nr_cnpj',
    'Valor': 'nr_valor'
}

cols_partido = {
    'Numero': 'nr_partido',
    'Sigla': 'sg_partido',
    'Nome': 'nm_partido'
}


def deps():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'deputados/deputados.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'NomeParlamentar', 'Matricula', 'IdDeputado', 'IdSPL', 'IdUA',
        'Partido', 'Sala', 'Andar', 'Telefone', 'Email', 'PlacaVeiculo',
        'Aniversario', 'Situacao'
    ]]
    dataset = dataset.rename(columns=cols_deps)
    save(dataset, 'dep')


def area():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'deputados/deputado_area_atuacao.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['IdDeputado', 'IdArea', 'NrOrdem']]
    dataset = dataset.rename(columns=cols_area)
    save(dataset, 'dep_areas')


def area_indice():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'deputados/areas_atuacao.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['Id', 'Nome']]
    dataset = dataset.rename(columns={'Id': 'id_area', 'Nome': 'nm_area'})
    save(dataset, 'dep_areas_indice')


def base():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'deputados/deputado_base_eleitoral.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['IdDeputado', 'IdBaseEleitoral', 'NrOrdem']]
    dataset = dataset.rename(columns=cols_base)
    save(dataset, 'dep_bases')


def base_indice():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'deputados/bases_eleitorais.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['Id', 'Nome']]
    dataset = dataset.rename(columns={'Id': 'id_base', 'Nome': 'nm_base'})
    save(dataset, 'dep_bases_indice')


def partido():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'deputados/partidos.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['Numero', 'Sigla', 'Nome']]
    dataset = dataset.rename(columns=cols_partido)
    save(dataset, 'dep_partidos_indice')


def gasto():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'deputados/despesas_gabinetes.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'Deputado', 'Matricula', 'Ano', 'Mes', 'Tipo',
        'Fornecedor', 'CNPJ', 'Valor'
    ]]
    dataset = dataset.rename(columns=cols_gastos)
    clean_expenses_categories(dataset)
    save(dataset, 'dep_gastos_cota')


def main():
    deps()
    area()
    area_indice()
    base()
    base_indice()
    partido()
    gasto()


if __name__ == '__main__':
    main()
