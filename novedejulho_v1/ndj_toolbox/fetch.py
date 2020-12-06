import os
from datetime import datetime
import xml.etree.ElementTree as ElementTree
from urllib.request import urlretrieve
from zipfile import ZipFile

from tqdm import tqdm
import pandas as pd

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
DATA_DIR = f'data_{TODAY}'


class ParseXml:
    """Faz análise de um xml local e processa em dataframe:

    >> ParseXmlRemote('arquivo.xml').process_data()

    :param xml_data: (var / str) arquivo de origem
    :return: (var) variável apontando para o dataframe
    """

    def __init__(self, xml_data):
        self.tree = ElementTree.parse(xml_data)
        self.root = self.tree.getroot()

    def parse_root(self, root=None):
        root = root if root else self.root
        yield from (self.parse_element(child) for child in iter(root))

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()

        new_values = {k: element.attrib.get(k) for k in element.keys()}
        parsed.update(new_values)
        if element.text:
            parsed[element.tag] = element.text

        for child in list(element):
            self.parse_element(child, parsed)

        return parsed

    def process_data(self):
        return pd.DataFrame(self.parse_root())


class ParseXmlRemote():
    """Faz análise de um xml remoto e processa em dataframe:

    >> ParseXmlRemote('http://...arquivo.xml').process_data()

    :param xml_data: (var / str) arquivo de origem
    :return: (var) variável apontando para o dataframe
    """

    def __init__(self, xml_data):
        self.root = ElementTree.XML(xml_data)

    def parse_root(self, root=None):
        root = root if root else self.root
        yield from (self.parse_element(child) for child in iter(root))

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()

        new_values = {k: element.attrib.get(k) for k in element.keys()}
        parsed.update(new_values)
        if element.text:
            parsed[element.tag] = element.text

        for child in list(element):
            self.parse_element(child, parsed)

        return parsed

    def process_data(self):
        return pd.DataFrame(self.parse_root())


def fetch_zip(url, arquivo_zip):
    """Baixa o arquivo zip de uma URL, descompacta, salva o arquivo
    descompactado na pasta correta e deleta o zip:

    >> fetch_zip('http://...arquivo.zip', 'arquivo.zip')
    'pasta_correta/arquivo.xml'

    :param url: (str) URL do arquivo zip
    :param name: (str) nome do arquivo zip a ser salvo
    :return: (str) caminho para o arquivo descompactado
    """
    urlretrieve(url, f'{DATA_DIR}/{arquivo_zip}')
    with ZipFile(f'{DATA_DIR}/{arquivo_zip}', 'r') as zip_file:
        zip_file.extractall(f'{DATA_DIR}')
    os.remove(f'{DATA_DIR}/{arquivo_zip}')


def save_file(dataset, name, extension):
    """Função auxiliar para a função 'save'. Formata o dataframe e
    parametriza as duas extensões:

    :param dataset: (var) dataframe a ser salvo
    :param name: (str) nome do arquivo
    :return: (str) a extensão .csv ou .xz
    """
    params = {'encoding': 'utf-8',
              'index': False,
              'sep': ','}
    if extension == 'xz':
        params['compression'] = 'xz'

    file_name = f'{name}.{extension}'
    dataset = dataset.apply(lambda x: x.str.lower() if (x.dtype == 'object')
                            else x)
    dataset = dataset.apply(lambda x: x.replace({
        '#nulo#': '',
        'null/null': ''
    }) if (x.dtype == 'object') else x)
    dataset.to_csv(os.path.join(DATA_DIR, file_name), **params)


def save(dataset, name):
    """Salva dataset em csv e xz, na pasta correta e com os parâmetros
    pré-estabelecidos:

    >> save(dataset, 'name')
    'pasta_correta/name.csv'
    'pasta_correta/name.xz'

    :param dataset: (var) variável com o dataframe do script
    :param name: (str) nome do arquivo
    :return: (str) caminho para o arquivo salvo
    """
    for extension in tqdm(('csv', 'xz'), desc=f'- {name}', ncols=100):
        save_file(dataset, name, extension)
