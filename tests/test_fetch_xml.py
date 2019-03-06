import os
import re
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ElementTree
from urllib.request import urlretrieve
from zipfile import ZipFile
import requests as req

import pandas as pd

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
DATA_DIR = f'data_{TODAY}'


class ParseXml:

    def __init__(self, xml_location, zip=False):
        self.xml_location = xml_location

        if not self.is_local:
            tree = ElementTree.XML(xml_location)
            self.root = tree.getroot()

        elif self.is_zipped:
            data = self.unzip()
            self.root = ElementTree.XML(data)

        else:
            self.root = ElementTree.XML(xml_location)

    @property
    def is_local(self):
        return not self.xml_location.lower().startswith('http')

    @property
    def is_zipped(self):
        return self.xml_location.lower().endswith('.zip')

    def unzip(self):
        url_pattern = re.compile(r'http|s:.*\w*\.zip$')
        zip_name = re.sub(url_pattern, r'\w*\.zip$', self.url)

        urlretrieve(self.url, f'{self.DATA_DIR}/{zip_name}')
        with ZipFile(f'{self.DATA_DIR}/{zip_name}', 'r') as zip_file:
            zip_file.extractall(f'{self.DATA_DIR}')
        os.remove(f'{self.DATA_DIR}/{zip_name}')

        for filename in Path(self.DATA_DIR).glob('*.xml'):
            self.xml_data = filename
            return filename

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


# class xml_df:
#
#    def __init__(self, xml_data):
#        self.root = ElementTree.XML(xml_data)
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

def test_fetch_xml():
    global url, dataset
    url_base = 'https://www.w3schools.com/xml/'
    url_file = 'cd_catalog.xml'
    url = url_base + url_file
    xml_data = req.get(url).content
    dataset = ParseXml(xml_data).process_data()


def test_rename_columns():
    global dataset
    dataset = dataset[[
        'TITLE', 'ARTIST', 'COUNTRY', 'COMPANY', 'PRICE', 'YEAR'
    ]]
    dataset = dataset.rename(columns={
        'TITLE': 'titulo',
        'ARTIST': 'artista',
        'COUNTRY': 'pais',
        'COMPANY': 'gravadora',
        'PRICE': 'preco',
        'YEAR': 'ano'
    })


def test_columns_names():
    assert list(dataset) == ['titulo', 'artista', 'pais',
                             'gravadora', 'preco', 'ano']


def test_columns_length():
    assert len(dataset['titulo']) == len(dataset['artista'])


def test_null_values():
    for i in dataset['preco']:
        assert i != ''


def test_sanitize_int():
    global dataset
    dataset['ano'] = dataset['ano'].astype('int64')


def test_int_values():
    for j in dataset['ano']:
        assert type(j) == int


def test_sanitize_float():
    global dataset
    dataset['preco'] = dataset['preco'].astype('float64')


def test_float_values():
    for k in dataset['preco']:
        assert type(k) == float


def test_type_str():
    for l in dataset['gravadora']:
        assert type(l) == str


def test_sum():
    assert dataset['preco'].sum() == 237.0


def test_count():
    assert dataset['titulo'].count() == 26
