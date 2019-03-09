import os
import xml.etree.ElementTree as ElementTree
from urllib.request import urlretrieve

import pandas as pd

f = urlretrieve('https://www.w3schools.com/xml/cd_catalog.xml',
                'cd_catalog.xml')


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
    dataset = ParseXml(f).process_data()


def test_sanitize_int():
    global dataset
    dataset['YEAR'] = dataset['YEAR'].astype('int64')


def test_int_values():
    for j in dataset['YEAR']:
        assert type(j) == int


def test_sanitize_float():
    global dataset
    dataset['PRICE'] = dataset['PRICE'].astype('float64')


def test_float_values():
    for k in dataset['PRICE']:
        assert type(k) == float


def test_sum():
    assert dataset['PRICE'].sum() == 237.0


def test_count():
    assert dataset['TITLE'].count() == 26


os.remove('cd_catalog.xml')
