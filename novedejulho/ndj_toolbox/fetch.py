import os
from datetime import datetime
import xml.etree.ElementTree as ElementTree
import glob
import csv
import sqlite3

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

def save_file(df, data_dir, name, extension):
    params = {'encoding': 'utf-8', 'index': False, 'sep': '\t'}
    if extension == 'xz':
        params['compression'] = 'xz'

    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    file_name = '{}-{}.{}'.format(today, name, extension)
    df.to_csv(os.path.join(data_dir, file_name), **params)


def save_files(df, data_dir, name):
    for extension in ('csv', 'xz'):
        save_file(df, data_dir, name, extension)


# Utilitário para criar db dos csv extraídos

def generate_db():
    for csvFile in glob.glob('data/*.csv'):
        file_name = os.path.basename(csvFile)
        with open(csvFile, mode='r', encoding='utf-8') as file_table:
            reader = csv.DictReader(file_table, delimiter='\t')
            fields = tuple(reader.fieldnames)
            con = sqlite3.connect('data/novedejulho.db')
            cur = con.cursor()
            cur.execute(f"CREATE TABLE '{file_name}' {fields};")
            reader_2 = csv.reader(file_table, delimiter='\t')
            for i in reader_2:
                i = tuple(i)
                cur.execute(f"INSERT INTO '{file_name}' VALUES {i};")
            con.commit()
    con.close()
