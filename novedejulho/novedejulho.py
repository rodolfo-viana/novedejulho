import os
from time import time

from ndj_toolbox.format import generate_db

IGNORE_LIST = ['__init__.py', 'novedejulho.py']

data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def retrieve_files():
    files = os.listdir('.')
    files = [f for f in files if '.py' in f and f not in IGNORE_LIST]

    for f in sorted(files):
        module_name = f.replace('.py', '')
        module = __import__(module_name)
        module.main()
        print(f"Fazendo o download de {module_name}...")


if __name__ == '__main__':
    start = time()
    print(f"Criando o diretório {data_dir}...")
    create_dir()
    retrieve_files()
    print("Agregando tabelas no arquivo novedejulho.db...")
    generate_db()
    end = time()
    print(
        f"Os dados estão na pasta {data_dir}.\nFinalizado em {end - start} segundos.")
