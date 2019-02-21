import os
from time import time
from datetime import datetime

from ndj_toolbox.format import generate_db

hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')

IGNORE_LIST = ['__init__.py', 'novedejulho.py']
DATA_DIR = f'data_{hoje}'


def create_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def retrieve_files():
    files = os.listdir('.')
    files = [f for f in files if '.py' in f and f not in IGNORE_LIST]

    for f in sorted(files):
        module_name = f.replace('.py', '')
        print(f"Fazendo o download de {module_name}...")
        module = __import__(module_name)
        module.main()


if __name__ == '__main__':
    start = time()
    print(f"Criando o diretório {DATA_DIR}...")
    create_dir()
    retrieve_files()
    print("Gerando o arquivo novedejulho.db...")
    generate_db()
    end = time()
    hora, resto = divmod(end - start, 3600)
    minutos, segundos = divmod(resto, 60)
    print("Finalizado em {:0>2}:{:0>2}:{:05.2f}.".format(int(hora), int(minutos), segundos))
