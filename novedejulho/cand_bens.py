import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile
import csv

import pandas as pd
from ndj_toolbox.fetch import save_files
from ndj_toolbox.format import (merge_dfs, sanitize_float)


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    url_base = 'http://agencia.tse.jus.br/estatistica/sead/odsele/bem_candidato/'
    arquivos = ['bem_candidato_2014', 'bem_candidato_2018']

    for arquivo in arquivos:
        url = url_base + arquivo + '.zip'
        urlretrieve(url, f'{DATA_DIR}/{arquivo}.zip')
        zip_file = ZipFile(f'{DATA_DIR}/{arquivo}.zip', 'r')
        zip_file.extract(f'{arquivo}_SP.csv', path=f'{DATA_DIR}')
        zip_file.close()
        os.remove(f'{DATA_DIR}/{arquivo}.zip')

        with open(f'{DATA_DIR}/candidato_bem.csv', 'a', newline='') as infile:
            writer = csv.writer(infile, delimiter=';')
            with open(f'{DATA_DIR}/{arquivo}_SP.csv', 'r') as original:
                reader = csv.reader(original, delimiter=';')
                next(reader, None)
                for row in reader:
                    writer.writerow(row)
        os.remove(f'{DATA_DIR}/{arquivo}_SP.csv')

    cols = [
        'dt_geracao', 'hh_geracao', 'ano_eleicao', 'cd_tipo_eleicao',
        'nm_tipo_eleicao', 'cd_eleicao', 'ds_eleicao', 'dt_eleicao', 'sg_uf',
        'sg_ue', 'nm_ue', 'sq_candidato', 'nr_ordem_candidato', 'cd_tp_bem',
        'ds_tp_bem', 'ds_bem', 'vlr_bem', 'dt_ultima_atualizacao',
        'hh_ultima_atualizacao'
    ]

    bens = pd.read_csv(f'{DATA_DIR}/candidato_bem.csv',
                       header=0,
                       names=cols,
                       encoding='latin-1',
                       sep=';')
    merge_dfs()

    save_files(dataset, 'candidatos_bens')
    os.remove(f'{DATA_DIR}/candidato_bem.csv')


if __name__ == '__main__':
    main()
