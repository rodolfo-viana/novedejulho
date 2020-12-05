import os
import json


def sanitize_float(x):
    """Altera vírgula por ponto para se adequar aos processadores:

    >> sanitize_float(x)
    'x = 10.99'

    :param i: (val) valor com vírgula
    :return: (val) valor com ponto
    """
    return float(x.get_text().strip().replace('.', '').replace(',', '.'))


def type_cols(df, io_file):
    """Tipa as colunas a partir do `json` e reorganiza dataframe:

    >> type_cols(df, io_file)

    :param df: (var) variável com o dataframe
    :param io_file: (file) `json` com as configurações
    :return: (var) dataframe tipado
    """
    with open(io_file, 'r') as f:
        columns = json.loads(f.read())

    dataset = df.rename(columns=columns[0])
    dataset = dataset.astype(columns[1])
    return dataset[[i for i in columns[1].keys()]]


def save(dataset, name):
    """Cria diretório 'data', se não houver, e salva `csv`:

    >> save('nome', dataset)

    :param dataset: (var) dataframe a ser salvo; default: 'dataset'
    :param name: (str) nome do arquivo
    :return: (file) arquivo `csv`
    """
    datadir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(datadir):
        os.mkdir(datadir)

    params = {'encoding': 'utf-8',
              'index': False,
              'sep': ','}
    fname = os.path.join(datadir, '{}.csv'.format(name))
    dataset.to_csv(fname, **params)
