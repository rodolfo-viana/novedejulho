import requests as req
import xml.etree.ElementTree as ElementTree

import pandas as pd


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


def test_fetch_xml():
    global dataset
    url = 'https://www.w3schools.com/xml/cd_catalog.xml'
    xml_data = req.get(url).content
    dataset = ParseXmlRemote(xml_data).process_data()


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


def test_str_values():
    for l in dataset['gravadora']:
        assert type(l) == str
