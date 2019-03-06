import os
from datetime import datetime
import xml.etree.ElementTree as ElementTree

import pandas as pd


# Utilitários para extrair dados de xml online

class xml_df:

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


# Utilitários para extrair dados de xml em arquivo local

class xml_df_internal:

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


# Utilitários para salvar os dados em csv comprimido e regular

def save_file(df, name, extension):
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    try:
        os.makedirs(DATA_DIR)
    except:
        pass

    params = {'encoding': 'utf-8',
              'index': False,
              'sep': ','}
    if extension == 'xz':
        params['compression'] = 'xz'

    file_name = '{}.{}'.format(name, extension)
    df.to_csv(os.path.join(DATA_DIR, file_name), **params)


def save_files(df, name):
    for extension in ('csv', 'xz'):
        save_file(df, name, extension)


########################################
#       NOVA VERSÃO (sem testes)       #
########################################
#
#import os
#import re
#from pathlib import Path
#from datetime import datetime
#import xml.etree.ElementTree as ElementTree
#from urllib.request import urlretrieve
#from zipfile import ZipFile
#
#import pandas as pd
#
#TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
#DATA_DIR = f'data_{TODAY}'
#
#
# class ParseXml:
#
#    def __init__(self, xml_location, zip=False):
#        self.xml_location = xml_location
#
#        if not self.is_local:
#            tree = ElementTree.XML(xml_location)
#            self.root = tree.getroot()
#
#        elif self.is_zipped:
#            data = self.unzip()
#            self.root = ElementTree.XML(data)
#
#        else:
#            self.root = ElementTree.XML(xml_location)
#
#    @property
#    def is_local(self):
#        return not self.xml_location.lower().startswith('http')
#
#    @property
#    def is_zipped(self):
#        return self.xml_location.lower().endswith('.zip')
#
#    def unzip(self):
#        url_pattern = re.compile(r'http|s:.*\w*\.zip$')
#        zip_name = re.sub(url_pattern, r'\w*\.zip$', self.url)
#
#        urlretrieve(self.url, f'{self.DATA_DIR}/{zip_name}')
#        with ZipFile(f'{self.DATA_DIR}/{zip_name}', 'r') as zip_file:
#            zip_file.extractall(f'{self.DATA_DIR}')
#        os.remove(f'{self.DATA_DIR}/{zip_name}')
#
#        for filename in Path(self.DATA_DIR).glob('*.xml'):
#            self.xml_data = filename
#            return filename
#
#    def parse_root(self, root=None):
#        root = root if root else self.root
#        yield from (self.parse_element(child) for child in iter(root))
#
#    def parse_element(self, element, parsed=None):
#        if parsed is None:
#            parsed = dict()
#
#        new_values = {k: element.attrib.get(k) for k in element.keys()}
#        parsed.update(new_values)
#        if element.text:
#            parsed[element.tag] = element.text
#
#        for child in list(element):
#            self.parse_element(child, parsed)
#
#        return parsed
#
#    def process_data(self):
#        return pd.DataFrame(self.parse_root())
#
#
# def save_file(dataset, name, extension):
#    params = {'encoding': 'utf-8',
#              'index': False,
#              'sep': ','}
#    if extension == 'xz':
#        params['compression'] = 'xz'
#
#    file_name = f'{name}.{extension}''
#    df.to_csv(os.path.join(DATA_DIR, file_name), **params)
#
#
# def save(dataset, name):
#    """Função para salvar dataset em csv e xz, na pasta correta e com os
#    parâmetros pré-estabelecidos:
#
#    >> save(dataset, 'name')
#    'pasta_correta/name.csv'
#    'pasta_correta/name.xz'
#
#    :param dataset: (var) variável com o dataframe do script
#    :param name: (str) nome do arquivo
#    :return: (str) caminho para o arquivo salvo
#    """
#    for extension in ('csv', 'xz'):
#        save_file(dataset, name, extension)
