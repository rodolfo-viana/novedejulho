# -*- coding: UTF-8 -*-

import os
import glob
import csv
import sqlite3
from time import time
from datetime import datetime

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
DATA_DIR = f'data_{TODAY}'
IGNORE_LIST = ['__init__.py', 'novedejulho.py']


def create_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def retrieve_files():
    scope = [
        'Candidatos:', 'Comissões:', 'Deputados:',
        'Documentos:', 'Legislações:', 'Servidores:'
    ]
    files = os.listdir('.')
    files = [f for f in files if '.py' in f and f not in IGNORE_LIST]

    for f, s in zip(sorted(files), sorted(scope)):
        module_name = f.replace('.py', '')
        module = __import__(module_name)
        print(f'{s}')
        module.main()


def generate_db():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'
    for csvFile in glob.glob(f'{DATA_DIR}/*.csv'):
        file_name = os.path.basename(csvFile)
        file_name = file_name[0:-4]
        with open(csvFile, mode='r', encoding='utf-8') as file_table:
            reader = csv.DictReader(file_table)
            fields = tuple(reader.fieldnames)
            con = sqlite3.connect(f'{DATA_DIR}/novedejulho.db')
            cur = con.cursor()
            cur.execute(f"CREATE TABLE '{file_name}' {fields};")
            reader_2 = csv.reader(file_table)
            for i in reader_2:
                for x in range(len(i)):
                    i[x] = i[x].replace("'", "")  # Para evitar conflito com a aspa de 'INSERT INTO'
                i = tuple(i)
                cur.execute(f"INSERT INTO '{file_name}' VALUES {i};")
            con.commit()
    con.close()


if __name__ == '__main__':
    start = time()
    print('\nNove de Julho - v0.3\nPor Rodolfo Viana e colaboradores')
    print('https://github.com/rodolfo-viana/novedejulho\n')
    print(f'Criando pasta "{DATA_DIR}"')
    create_dir()
    print('Pasta criada\nIniciando download')
    retrieve_files()
    print('Dados baixados\nGerando o arquivo "novedejulho.db"')
    generate_db()
    end = time()
    h, r = divmod(end - start, 3600)
    m, s = divmod(r, 60)
    print('Arquivo gerado')
    print('Finalizado em {:0>2}:{:0>2}:{:05.2f}.'.format(int(h), int(m), s))
