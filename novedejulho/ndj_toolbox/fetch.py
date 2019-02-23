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
