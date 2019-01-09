# Este código é inspirado no script 'helpers.py', usado em serenata-toolbox,
# componente da Operação Serenata de Amor. Conheça o projeto aqui:
# https://github.com/okfn-brasil/serenata-de-amor
# https://github.com/okfn-brasil/serenata-toolbox

import os
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd

XZ_PARAMS = {
    'compression': 'xz',
    'encoding': 'utf-8',
    'index': False
}

CSV_PARAMS = {
    'encoding': 'utf-8',
    'index': False
}


# Utilitários para extrair dados de xml

class xml_df:

    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)

    def parse_root(self, root):
        return [self.parse_element(child) for child in iter(root)]

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()
        for key in element.keys():
            parsed[key] = element.attrib.get(key)
        if element.text:
            parsed[element.tag] = element.text
        for child in list(element):
            self.parse_element(child, parsed)
        return parsed

    def process_data(self):
        structure_data = self.parse_root(self.root)
        return pd.DataFrame(structure_data)


# Utilitários para salvar os dados em csv comprimido e regular

def save_xz(df, data_dir, name):
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    file_path = os.path.join(data_dir, '{}-{}.xz'.format(today, name))
    df.to_csv(file_path, **XZ_PARAMS)


def save_csv(df, data_dir, name):
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    file_path = os.path.join(data_dir, '{}-{}.csv'.format(today, name))
    df.to_csv(file_path, **CSV_PARAMS)
