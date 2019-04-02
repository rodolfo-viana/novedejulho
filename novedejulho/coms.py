import requests as req

from ndj_toolbox.fetch import (ParseXmlRemote, save)
from ndj_toolbox.format import remove_dep

cols_com = {
    'IdComissao': 'id_comissao',
    'NomeComissao': 'nm_comissao',
    'SiglaComissao': 'sg_comissao',
    'DescricaoComissao': 'ds_comissao',
    'DataFimComissao': 'dt_fim_comissao'
}

cols_delib = {
    'IdReuniao': 'id_reuniao',
    'IdDocumento': 'id_documento',
    'IdPauta': 'id_pauta',
    'NrOrdem': 'nr_ordem',
    'DataInclusao': 'dt_inclusao',
    'DataSaida': 'dt_saida',
    'Deliberacao': 'ds_deliberacao',
    'IdDeliberacao': 'id_deliberacao'
}

cols_membros = {
    'SiglaComissao': 'sg_comissao',
    'IdComissao': 'id_comissao',
    'NomeMembro': 'nm_deputado',
    'IdMembro': 'id_spl',
    'Papel': 'ds_papel',
    'IdPapel': 'id_papel',
    'Efetivo': 'tx_efetivo',
    'DataInicio': 'dt_inicio',
    'DataFim': 'dt_fim'
}

cols_pres = {
    'IdReuniao': 'id_reuniao',
    'IdPauta': 'id_pauta',
    'IdDeputado': 'id_deputado',
    'Deputado': 'nm_deputado',
    'IdComissao': 'id_comissao',
    'SiglaComissao': 'sg_comissao',
    'DataReuniao': 'dt_comissao'
}

cols_reun = {
    'IdReuniao': 'id_reuniao',
    'IdComissao': 'id_comissao',
    'IdPauta': 'id_pauta',
    'NrLegislatura': 'nr_legislatura',
    'NrConvocacao': 'nr_convocacao',
    'TipoConvocacao': 'tp_convocacao',
    'Data': 'dt_reuniao',
    'CodSituacao': 'cd_situacao',
    'Situacao': 'ds_situacao',
    'Presidente': 'nm_presidente'
}

cols_voto = {
    'IdReuniao': 'id_reuniao',
    'IdPauta': 'id_pauta',
    'IdComissao': 'id_comissao',
    'IdDocumento': 'id_documento',
    'IdDeputado': 'id_deputado',
    'Deputado': 'nm_deputado',
    'TipoVoto': 'tp_voto',
    'Voto': 'ds_voto'
}


def coms():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/comissoes.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'IdComissao', 'NomeComissao', 'SiglaComissao', 'DescricaoComissao',
        'DataFimComissao'
    ]]
    dataset = dataset.rename(columns=cols_com)
    save(dataset, 'com')


def deliberacoes():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/comissoes_permanentes_deliberacoes.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'IdReuniao', 'IdDocumento', 'IdPauta', 'NrOrdem', 'DataInclusao',
        'DataSaida', 'Deliberacao', 'IdDeliberacao'
    ]]
    dataset = dataset.rename(columns=cols_delib)
    save(dataset, 'com_deliberacoes')


def membros():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/comissoes_membros.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'SiglaComissao', 'IdComissao', 'NomeMembro', 'IdMembro', 'Papel',
        'IdPapel', 'Efetivo', 'DataInicio', 'DataFim'
    ]]
    dataset = dataset.rename(columns=cols_membros)
    save(dataset, 'com_membros')


def presencas():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/comissoes_permanentes_presencas.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'IdReuniao', 'IdPauta', 'IdDeputado', 'Deputado',
        'IdComissao', 'SiglaComissao', 'DataReuniao'
    ]]
    dataset = dataset.rename(columns=cols_pres)
    save(dataset, 'com_presencas')


def reunioes():
    url_base = 'http://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/comissoes_permanentes_reunioes.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'IdReuniao', 'IdComissao', 'IdPauta',
        'NrLegislatura', 'NrConvocacao', 'TipoConvocacao',
        'Data', 'CodSituacao', 'Situacao', 'Presidente'
    ]]
    dataset = dataset.rename(columns=cols_reun)
    save(remove_dep(dataset), 'com_reunioes')


def votacoes():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/comissoes_permanentes_votacoes.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[[
        'IdReuniao', 'IdPauta', 'IdComissao', 'IdDocumento',
        'IdDeputado', 'Deputado', 'TipoVoto', 'Voto'
    ]]
    dataset = dataset.rename(columns=cols_voto)
    save(dataset, 'com_votacoes')


def main():
    coms()
    deliberacoes()
    membros()
    presencas()
    reunioes()
    votacoes()


if __name__ == '__main__':
    main()
