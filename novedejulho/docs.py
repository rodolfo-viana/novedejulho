import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile
import requests as req

from ndj_toolbox.fetch import (ParseXml, ParseXmlRemote, save)
from ndj_toolbox.format import remove_break_line

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
DATA_DIR = f'data_{TODAY}'

cols_docs = {
    'IdDocumento': 'id_documento',
    'CodOriginalidade': 'cd_originalidade',
    'AnoLegislativo': 'tx_ano_legislativo',
    'DtEntradaSistema': 'dt_apresentacao',
    'DtPublicacao': 'dt_publicacao',
    'IdNatureza': 'id_natureza',
    'NroLegislativo': 'nr_legislativo',
    'Ementa': 'tx_ementa'
}

cols_autores = {
    'IdDocumento': 'id_documento',
    'IdAutor': 'id_autor',
    'NomeAutor': 'nm_autor'
}

cols_naturezas = {
    'idNatureza': 'id_natureza',
    'nmNatureza': 'nm_natureza',
    'sgNatureza': 'sg_natureza',
    'tpNatureza': 'tp_natureza'
}

cols_palavras = {
    'IdDocumento': 'id_documento',
    'IdPalavra': 'id_palavra'
}

cols_pal_chave = {
    'IdPalavra': 'id_palavra',
    'Palavra': 'tx_termo',
    'PalavraSemAcento': 'tx_termo_sem_acento'
}

cols_pareceres = {
    'AnoParecer': 'tx_ano_parecer',
    'Data': 'dt_parecer',
    'IdComissao': 'id_comissao',
    'SiglaComissao': 'sg_comissao',
    'IdDocumento': 'id_documento',
    'IdParecer': 'id_parecer',
    'IdTipoParecer': 'id_tp_parecer',
    'TipoParecer': 'tp_parecer',
    'NrParecer': 'nr_parecer',
    'TpParecer': 'cat_parecer',
    'Descricao': 'ds_parecer',
    'AdReferendum': 'tx_adreferendum',
    'RelatorEspecial': 'tx_relator_especial',
    'VotoVencido': 'tx_voto_vencido',
    'URL': 'tx_url'
}

cols_pareceres_tp = {
    'IdTipoParcer': 'id_tp_parecer',
    'TipoParecer': 'tp_parecer'
}

cols_andam_atual = {
    'IdDocumento': 'id_documento',
    'Data': 'dt_tramitacao',
    'NrOrdem': 'nr_ordem',
    'Descricao': 'ds_andamento',
    'IdTpAndamento': 'id_tp_andamento',
    'TpAndamento': 'tp_andamento',
    'IdEtapa': 'id_etapa',
    'NmEtapa': 'nm_etapa',
    'IdComissao': 'id_comissao',
    'SiglaComissao': 'sg_comissao'
}

cols_tramit_regime = {
    'IdDocumento': 'id_documento',
    'IdRegime': 'id_regime',
    'NomeRegime': 'nm_regime',
    'DataInicio': 'dt_inicio',
    'DataFim': 'dt_fim'
}


def fetch_zip(url, arquivo_zip):
    urlretrieve(url, f'{DATA_DIR}/{arquivo_zip}')
    with ZipFile(f'{DATA_DIR}/{arquivo_zip}', 'r') as zip_file:
        zip_file.extractall(f'{DATA_DIR}')
    os.remove(f'{DATA_DIR}/{arquivo_zip}')


def docs():
    url_base = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
    arquivo_zip = 'proposituras.zip'
    url = url_base + arquivo_zip

    arquivo_xml = 'proposituras.xml'

    fetch_zip(url, arquivo_zip)
    xml_data = f'{DATA_DIR}/{arquivo_xml}'

    dataset = ParseXml(xml_data).process_data()
    dataset = dataset[[
        'AnoLegislativo', 'CodOriginalidade', 'Ementa', 'DtEntradaSistema',
        'DtPublicacao', 'IdDocumento', 'IdNatureza', 'NroLegislativo'
    ]]
    dataset = dataset.rename(columns=cols_docs)
    save(dataset, 'doc')
    os.remove(xml_data)


def autores():
    url_base = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
    arquivo_zip = 'documento_autor.zip'
    url = url_base + arquivo_zip

    arquivo_xml = 'documento_autor.xml'

    fetch_zip(url, arquivo_zip)
    xml_data = f'{DATA_DIR}/{arquivo_xml}'

    dataset = ParseXml(xml_data).process_data()
    dataset = dataset[['IdAutor', 'IdDocumento', 'NomeAutor']]
    dataset = dataset.rename(columns=cols_autores)
    save(dataset, 'doc_autores_indice')
    os.remove(xml_data)


def naturezas():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/naturezasSpl.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['idNatureza', 'nmNatureza', 'sgNatureza', 'tpNatureza']]
    dataset = dataset.rename(columns=cols_naturezas)
    save(dataset, 'doc_naturezas_indice')


def palavras():
    url_base = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
    arquivo_zip = 'documento_palavras.zip'
    url = url_base + arquivo_zip

    arquivo_xml = 'documento_palavras.xml'

    fetch_zip(url, arquivo_zip)
    xml_data = f'{DATA_DIR}/{arquivo_xml}'

    dataset = ParseXml(xml_data).process_data()
    dataset = dataset[['IdDocumento', 'IdPalavra']]
    dataset = dataset.rename(columns=cols_palavras)
    save(dataset, 'doc_palavras')
    os.remove(xml_data)


def palavras_chave():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/palavras_chave.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['IdPalavra', 'Palavra', 'PalavraSemAcento']]
    dataset = dataset.rename(columns=cols_pal_chave)
    save(dataset, 'doc_palavras_indice')


def pareceres():
    url_base = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
    arquivo_zip = 'propositura_parecer.zip'
    url = url_base + arquivo_zip

    arquivo_xml = 'propositura_parecer.xml'

    fetch_zip(url, arquivo_zip)
    xml_data = f'{DATA_DIR}/{arquivo_xml}'

    dataset = ParseXml(xml_data).process_data()
    dataset = dataset[[
        'AnoParecer', 'Descricao', 'Data', 'AdReferendum',
        'RelatorEspecial', 'VotoVencido', 'IdComissao',
        'IdDocumento', 'IdParecer', 'IdTipoParecer', 'TipoParecer',
        'NrParecer', 'SiglaComissao', 'TpParecer', 'URL'
    ]]
    dataset = dataset.rename(columns=cols_pareceres)
    save(dataset, 'doc_pareceres')
    os.remove(xml_data)


def pareceres_tp():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/tipo_parecer.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['IdTipoParcer', 'TipoParecer']]
    dataset = dataset.rename(columns=cols_pareceres_tp)
    save(dataset, 'doc_pareceres_tp_indice')


def andamento_atual():
    url_base = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
    arquivo_zip = 'documento_andamento_atual.zip'
    url = url_base + arquivo_zip

    arquivo_xml = 'documento_andamento_atual.xml'

    fetch_zip(url, arquivo_zip)
    xml_data = f'{DATA_DIR}/{arquivo_xml}'

    dataset = ParseXml(xml_data).process_data()
    dataset = dataset[[
        'IdDocumento', 'Data', 'NrOrdem', 'Descricao',
        'IdTpAndamento', 'TpAndamento', 'IdEtapa',
        'NmEtapa', 'IdComissao', 'SiglaComissao'
    ]]
    dataset = dataset.rename(columns=cols_andam_atual)
    dataset['ds_andamento'] = dataset['ds_andamento'].apply(remove_break_line)
    save(dataset, 'doc_andamento')
    os.remove(xml_data)


def tramitacao_regime():
    url_base = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
    arquivo_zip = 'documento_regime.zip'
    url = url_base + arquivo_zip

    arquivo_xml = 'documento_regime.xml'

    fetch_zip(url, arquivo_zip)
    xml_data = f'{DATA_DIR}/{arquivo_xml}'

    dataset = ParseXml(xml_data).process_data()
    dataset = dataset[[
        'IdDocumento', 'IdRegime', 'NomeRegime', 'DataInicio', 'DataFim'
    ]]
    dataset = dataset.rename(columns=cols_tramit_regime)
    save(dataset, 'doc_tramitacao_regime')
    os.remove(xml_data)


def main():
    docs()
    autores()
    naturezas()
    palavras()
    palavras_chave()
    pareceres()
    pareceres_tp()
    andamento_atual()
    tramitacao_regime()


if __name__ == '__main__':
    main()
