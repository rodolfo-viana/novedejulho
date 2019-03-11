import requests as req

from ndj_toolbox.fetch import (ParseXmlRemote, save)

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

dict_gasto = {
    'A - COMBUSTÍVEIS E LUBRIFICANTES': 'COMBUSTÍVEIS E LUBRIFICANTES',
    'B - LOCAÇÃO E MANUT DE BENS MÓVEIS E IMÓVEIS, CONDOMÍNIOS E OUTROS': 'LOCAÇÃO E MANUTENÇÃO DE BENS MÓVEIS, IMÓVEIS E CONDOMÍNIO',
    'C - MATERIAIS E SERVIÇOS DE MANUT E CONSERV DE VEÍCULOS ; PEDÁGIOS': 'MANUTENÇÃO DE VEÍCULOS E PEDÁGIOS',
    'D - MATERIAIS E SERVIÇOS GRÁFICOS, DE CÓPIAS  E REPRODUÇÃO DE DOCS': 'SERVIÇOS GRÁFICOS',
    'E - MATERIAIS DE ESCRITÓRIO E OUTROS MATERIAIS DE CONSUMO': 'MATERIAL DE ESCRITÓRIO',
    'F - SERVIÇOS TÉCNICOS PROFISSIONAIS (CONSULTORIA, PESQUISAS ETC)': 'SERVIÇOS TÉCNICOS E CONSULTORIAS',
    'G - ASSINATURAS DE PERIÓDICOS, PUBLICAÇÕES E INTERNET': 'ASSINATURA DE JORNAIS, REVISTAS E INTERNET',
    'H - SERV.UTIL.PÚBLICA (TELEF.MÓVEL/FIXA, ENERGIA, ÁGUA, GÁS ETC)': 'TELEFONE, ENERGIA, ÁGUA E OUTROS SERVIÇOS',
    'I - HOSPEDAGEM, ALIMENTAÇÃO E DESPESAS DE LOCOMOÇÃO': 'ALIMENTAÇÃO, HOSPEDAGEM E LOCOMOÇÃO',
    'J - SERVIÇOS DE COMUNICAÇÃO': 'SERVIÇOS DE COMUNICAÇÃO',
    'K - LOCAÇÃO DE BENS MÓVEIS': 'LOCAÇÃO DE BENS MÓVEIS',
    'L - LOCAÇÃO DE BENS IMÓVEIS': 'LOCAÇÃO DE IMÓVEIS',
    'M - MANUTENÇÃO DE BENS MÓVEIS,  IMÓVEIS, CONDOMÍNIOS E OUTROS': 'MANUTENÇÃO DE BENS MÓVEIS, IMÓVEIS E CONDOMÍNIO',
    'N - MORADIA': 'MORADIA'
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
    dataset['tp_categoria'].replace(dict_gasto, inplace=True)
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
