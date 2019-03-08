import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile
import requests as req

from ndj_toolbox.fetch import (ParseXml, ParseXmlRemote, save)
from ndj_toolbox.format import remove_break_line

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
DATA_DIR = f'data_{TODAY}'

cols_legs = {
    'IdNorma': 'id_norma',
    'Numero': 'nr_norma',
    'Ano': 'tx_ano',
    'IdTipo': 'id_tipo',
    'Data': 'dt_norma',
    'Situacao': 'tx_situacao',
    'Ementa': 'tx_ementa',
    'Autores': 'tx_autores',
    'CadDO': 'nr_caderno_do',
    'PagDO': 'nr_pagina_do',
    'DataDO': 'dt_publicacao_do',
    'URLDO': 'url_do',
    'URLFicha': 'url_ficha',
    'URLIntegra': 'url_integra',
    'URLCompilado': 'url_compilado',
    'Promulg': 'tx_promulg',
    'Ambito': 'tx_ambito'
}

cols_anota = {
    'IdNorma': 'id_norma',
    'NumNormaRel': 'nr_norma_relacionada',
    'DataNormaRel': 'dt_norma_relacionada',
    'TipoNormaRel': 'tp_norma_relacionada',
    'DsRel': 'ds_anotacao',
    'DsOrigem': 'ds_origem',
    'IdTipoRel': 'id_tipo',
    'NumComplNormaRel': 'nr_compl'
}

cols_subtemas = {
    'IdSubTema': 'id_subtema',
    'SubTema': 'ds_subtema'
}

cols_tipos = {
    'IdTipo': 'id_tp_norma',
    'DsTipo': 'ds_tp_norma'
}


def fetch_zip(url, arquivo_zip):
    urlretrieve(url, f'{DATA_DIR}/{arquivo_zip}')
    with ZipFile(f'{DATA_DIR}/{arquivo_zip}', 'r') as zip_file:
        zip_file.extractall(f'{DATA_DIR}')
    os.remove(f'{DATA_DIR}/{arquivo_zip}')


def legs():
    url_base = 'http://www.al.sp.gov.br/repositorioDados/legislacao/'
    arquivo_zip = 'legislacao_normas.zip'
    url = url_base + arquivo_zip

    arquivo_xml = 'legislacao_normas.xml'

    fetch_zip(url, arquivo_zip)
    xml_data = f'{DATA_DIR}/{arquivo_xml}'

    dataset = ParseXml(xml_data).process_data()
    dataset = dataset[[
        'IdNorma', 'Numero', 'Ano', 'IdTipo', 'Data', 'Situacao', 'Ementa',
        'Autores', 'CadDO', 'PagDO', 'DataDO', 'URLDO', 'URLFicha',
        'URLIntegra', 'URLCompilado', 'Promulg', 'Ambito'
    ]]
    dataset = dataset.rename(columns=cols_legs)
    dataset['tx_ementa'] = dataset['tx_ementa'].apply(remove_break_line)
    save(dataset, 'leg')
    os.remove(xml_data)


def anotacoes():
    url_base = 'http://www.al.sp.gov.br/repositorioDados/legislacao/'
    arquivo_zip = 'legislacao_norma_anotacoes.zip'
    url = url_base + arquivo_zip

    arquivo_xml = 'legislacao_norma_anotacoes.xml'

    fetch_zip(url, arquivo_zip)
    xml_data = f'{DATA_DIR}/{arquivo_xml}'

    dataset = ParseXml(xml_data).process_data()
    dataset = dataset[[
        'IdNorma', 'NumNormaRel', 'DataNormaRel', 'TipoNormaRel', 'DsRel',
        'DsOrigem', 'IdTipoRel', 'NumComplNormaRel'
    ]]
    dataset = dataset.rename(columns=cols_anota)
    save(dataset, 'leg_anotacoes')
    os.remove(xml_data)


def subtemas():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/legislacao/'
    url_file = 'legislacao_subtemas.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['IdSubTema', 'SubTema']]
    dataset = dataset.rename(columns=cols_subtemas)
    save(dataset, 'doc_subtemas_indice')


def temas():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/legislacao/'
    url_file = 'legislacao_temas.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['IdTema', 'Tema']]
    dataset = dataset.rename(columns={'IdTema': 'id_tema', 'Tema': 'ds_tema'})
    save(dataset, 'doc_temas_indice')


def tipos():
    url_base = 'https://www.al.sp.gov.br/repositorioDados/legislacao/'
    url_file = 'legislacao_tipo_normas.xml'
    url = url_base + url_file
    xml_data = req.get(url).content

    dataset = ParseXmlRemote(xml_data).process_data()
    dataset = dataset[['IdTipo', 'DsTipo']]
    dataset = dataset.rename(columns=cols_tipos)
    save(dataset, 'doc_tipos_indice')


def main():
    legs()
    anotacoes()
    subtemas()
    temas()
    tipos()


if __name__ == '__main__':
    main()
