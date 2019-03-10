import os
from time import time
from datetime import datetime

from tqdm import tqdm

from ndj_toolbox.format import generate_db

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
DATA_DIR = f'data_{TODAY}'
IGNORE_LIST = ['__init__.py', 'novedejulho.py']


def create_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def retrieve_files():
    files = os.listdir('.')
    files = [f for f in files if '.py' in f and f not in IGNORE_LIST]

    for f in sorted(files):
        module_name = f.replace('.py', '')
        for module in tqdm(module_name, desc=f'{module_name}', ncols=100):
            module = __import__(module_name)
            module.main()


if __name__ == '__main__':
    start = time()
    print('\nNove de Julho - v0.3\nPor Rodolfo Viana e colaboradores')
    print('https://github.com/rodolfo-viana/novedejulho\n')
    print(f'Criando pasta "{DATA_DIR}"')
    create_dir()
    print('Pasta criada\nFazendo download de dados')
    retrieve_files()
    print('Dados baixados\nGerando o arquivo "novedejulho.db"')
    generate_db()
    end = time()
    hora, resto = divmod(end - start, 3600)
    minutos, segundos = divmod(resto, 60)
    print('Arquivo gerado')
    print('Execução concluída em {:0>2}:{:0>2}:{:05.2f}.'.format(int(hora),
                                                                 int(minutos),
                                                                 segundos)
          )
