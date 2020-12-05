import xml.etree.ElementTree as ElementTree
import pandas as pd


class ParseXml:
    """Faz análise de um xml (remoto ou local) e processa em dataframe:

    >> ParseXml('arquivo.xml').process()

    :param xml_data: (var/str) arquivo de origem
    :return: (var) dataframe
    """

    def __init__(self, xml_data):
        try:
            self.root = ElementTree.XML(xml_data)
        except ElementTree.ParseError:
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

    def process(self):
        return pd.DataFrame(self.parse_root())
