import os
from datetime import datetime
import xml.etree.ElementTree as ElementTree

import pandas as pd

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
DATA_DIR = f'data_{TODAY}'


class ParseXml:

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


def save_file(dataset, name, extension):
    params = {'encoding': 'utf-8',
              'index': False,
              'sep': ','}
    if extension == 'xz':
        params['compression'] = 'xz'

    file_name = f'{name}.{extension}'
    dataset.to_csv(os.path.join(DATA_DIR, file_name), **params)


def save(dataset, name):
    """Função para salvar dataset em csv e xz, na pasta correta e com os
    parâmetros pré-estabelecidos:

    >> save(dataset, 'name')
    'pasta_correta/name.csv'
    'pasta_correta/name.xz'

    :param dataset: (var) variável com o dataframe do script
    :param name: (str) nome do arquivo
    :return: (str) caminho para o arquivo salvo
    """
    for extension in ('csv', 'xz'):
        save_file(dataset, name, extension)
