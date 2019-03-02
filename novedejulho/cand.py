import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile
import csv

import pandas as pd
from ndj_toolbox.fetch import save_files


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    url_base = 'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/'
    arquivos = ['consulta_cand_2014', 'consulta_cand_2018']

    for arquivo in arquivos:
        url = url_base + arquivo + '.zip'
        urlretrieve(url, f'{DATA_DIR}/{arquivo}.zip')
        zip_file = ZipFile(f'{DATA_DIR}/{arquivo}.zip', 'r')
        zip_file.extract(f'{arquivo}_SP.csv', path=f'{DATA_DIR}')
        zip_file.close()
        os.remove(f'{DATA_DIR}/{arquivo}.zip')

        with open(f'{DATA_DIR}/candidato_deputados.csv', 'a', newline='') as infile:
            writer = csv.writer(infile, delimiter=';')
            with open(f'{DATA_DIR}/{arquivo}_SP.csv', 'r') as original:
                reader = csv.reader(original, delimiter=';')
                next(reader, None)
                for row in reader:
                    writer.writerow(row)
        os.remove(f'{DATA_DIR}/{arquivo}_SP.csv')

    cols = [
        'dt_geracao', 'hh_geracao', 'ano_eleicao', 'cd_tipo_eleicao',
        'nm_tipo_eleicao', 'nr_turno', 'cd_eleicao', 'ds_eleicao',
        'dt_eleicao', 'tp_abrangencia', 'sg_uf', 'sg_ue', 'nm_ue', 'cd_cargo',
        'ds_cargo', 'sq_candidato', 'nr_candidato', 'nm_candidato',
        'nm_urna_candidato', 'nm_social_candidato', 'nr_cpf_candidato',
        'nm_email', 'cd_situacao_candidatura', 'ds_situacao_candidatura',
        'cd_detalhe_situacao_cand', 'ds_detalhe_situacao_cand',
        'tp_agremiacao', 'nr_partido', 'sg_partido', 'nm_partido',
        'sq_coligacao', 'nm_coligacao', 'ds_composicao_coligacao',
        'cd_nacionalidade', 'ds_nacionalidade', 'sg_uf_nascimento',
        'cd_municipio_nascimento', 'nm_municipio_nascimento', 'dt_nascimento',
        'nr_idade_data_posse', 'nr_titulo_eleitoral_candidato', 'cd_genero',
        'ds_genero', 'cd_grau_instrucao', 'ds_grau_instrucao',
        'cd_estado_civil', 'ds_estado_civil', 'cd_cor_raca', 'ds_cor_raca',
        'cd_ocupacao', 'ds_ocupacao', 'nr_despesa_max_campanha',
        'cd_sit_tot_turno', 'ds_sit_tot_turno', 'st_reeleicao',
        'st_declarar_bens', 'nr_protocolo_candidatura', 'nr_processo'
    ]

    dataset = pd.read_csv(f'{DATA_DIR}/candidato_deputados.csv',
                          header=0,
                          names=cols,
                          encoding='latin-1',
                          sep=';')
    dataset = dataset[dataset['ds_cargo'] == 'DEPUTADO ESTADUAL']

    save_files(dataset, 'deputados_eleicoes')
    # Precisar URGENTEMENTE formatar esses dados
    os.remove(f'{DATA_DIR}/candidato_deputados.csv')


if __name__ == '__main__':
    main()
