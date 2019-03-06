import os
import re
from datetime import datetime
import xml.etree.ElementTree as ElementTree
from urllib.request import urlretrieve
from zipfile import ZipFile

import pandas as pd


class Parse_xml:

    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

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


class Parse_xml_external(Parse_xml):

    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.root = ElementTree.XML(xml_data)


class Retrieve_zip(Parse_xml):

    def __init__(self, url, xml_data):
        super().__init__(xml_data)
        self.url = url

    def unzip(self):
        url_pattern = re.compile(r'http|s:.*\w*\.zip$')
        zip_name = re.sub(url_pattern, r'\w*\.zip$', self.url)
        urlretrieve(self.url, f'{self.DATA_DIR}/{zip_name}')
        zip_file = ZipFile(f'{self.DATA_DIR}/{zip_name}', 'r')
        zip_file.extractall(f'{self.DATA_DIR}')
        zip_file.close()
        for file in os.listdir(f'{self.DATA_DIR}'):
            if file.endswith('.xml'):
                self.xml_data = file
        os.remove(f'{self.DATA_DIR}/{zip_name}')

        return self.xml_data


def save(name):
    '''
    Função para salvar dataset em csv, na pasta
    correta e com os parâmetros pré-estabelecidos
    USO:
        >> save('name')
    INPUT:
        (str) 'name': nome do arquivo
    OUTPUT:
        (file) 'pasta_correta/file_name.csv'
    '''

    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    file_name = f'{name}.csv'

    params = {'encoding': 'utf-8',
              'index': False,
              'sep': ','}
    dataset.to_csv(os.path.join(DATA_DIR, file_name), **params)
