import requests as req
import xml.etree.ElementTree as ElementTree

import pandas as pd


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


def test_fetch_xml():
    global url, dataset
    url_base = 'https://www.w3schools.com/xml/'
    url_file = 'cd_catalog.xml'
    url = url_base + url_file
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()


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


def test_type_str():
    for j in dataset['gravadora']:
        assert type(j) == str


def test_sanitize_int():
    return int(k for k in dataset['ano'])
    for k in dataset['ano']:
        assert type(k) == int


def test_sanitize_float():
    return float(l for l in dataset['preco'])
    for l in dataset['preco']:
        assert type(l) == float


def test_sum():
    return float(m for m in dataset['preco'])
    assert dataset['preco'].sum() == 270.0


def test_count():
    assert dataset['titulo'].count() == 26
