import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile
import csv

import pandas as pd
from ndj_toolbox.fetch import save

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')
DATA_DIR = f'data_{TODAY}'

cols_cands = [
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
    'cd_ocupacao', 'ds_ocupacao', 'vlr_despesa_max_campanha',
    'cd_sit_tot_turno', 'ds_sit_tot_turno', 'st_reeleicao',
    'st_declarar_bens', 'nr_protocolo_candidatura', 'nr_processo'
]

drop_cols_cands = [
    'cd_tipo_eleicao', 'nr_turno', 'cd_eleicao', 'sg_uf', 'cd_cargo',
    'cd_situacao_candidatura', 'cd_detalhe_situacao_cand', 
    'cd_nacionalidade', 'cd_genero', 'cd_grau_instrucao', 'cd_estado_civil', 
    'cd_cor_raca', 'cd_ocupacao', 'cd_sit_tot_turno'
]

cols_bens = [
    'dt_geracao', 'hh_geracao', 'ano_eleicao', 'cd_tipo_eleicao',
    'nm_tipo_eleicao', 'cd_eleicao', 'ds_eleicao', 'dt_eleicao', 'sg_uf',
    'sg_ue', 'nm_ue', 'sq_candidato', 'nr_ordem_candidato', 'cd_tp_bem',
    'ds_tp_bem', 'ds_bem', 'vlr_bem', 'dt_ultima_atualizacao',
    'hh_ultima_atualizacao'
]


drop_cols_bens = [
    'cd_tp_bem', 'dt_geracao_y', 'hh_geracao_y', 'ano_eleicao_y', 'cd_tipo_eleicao',
    'nm_tipo_eleicao_y', 'cd_eleicao', 'ds_eleicao_y', 'dt_eleicao_y', 
    'sg_uf', 'sg_ue_y', 'nm_ue_y', 'ds_cargo', 'nm_email', 
    'ds_situacao_candidatura', 'ds_detalhe_situacao_cand', 'tp_agremiacao', 
    'nr_partido', 'sg_partido', 'nm_partido', 'sq_coligacao', 'nm_coligacao', 
    'ds_composicao_coligacao', 'ds_nacionalidade', 'sg_uf_nascimento',
    'cd_municipio_nascimento', 'nm_municipio_nascimento', 'dt_nascimento',
    'nr_idade_data_posse', 'nr_titulo_eleitoral_candidato', 'ds_genero', 
    'ds_grau_instrucao', 'ds_estado_civil', 'ds_cor_raca', 'ds_ocupacao', 
    'vlr_despesa_max_campanha', 'ds_sit_tot_turno', 'st_reeleicao', 
    'st_declarar_bens', 'nr_protocolo_candidatura', 'nr_processo', 
    'dt_ultima_atualizacao', 'hh_ultima_atualizacao'
]


def deps():
    url_base = 'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/'
    arquivos = ['consulta_cand_2014', 'consulta_cand_2018']

    with open(f'{DATA_DIR}/candidato_deputados.csv', 'a', newline='', encoding='latin-1') as infile:
        writer = csv.writer(infile, delimiter=';')

        for arquivo in arquivos:
            url = url_base + arquivo + '.zip'
            urlretrieve(url, f'{DATA_DIR}/{arquivo}.zip')
            with ZipFile(f'{DATA_DIR}/{arquivo}.zip', 'r') as zip_file:
                zip_file.extract(f'{arquivo}_SP.csv', path=f'{DATA_DIR}')
            os.remove(f'{DATA_DIR}/{arquivo}.zip')

            with open(f'{DATA_DIR}/{arquivo}_SP.csv', 'r', encoding='latin-1') as original:
                reader = csv.reader(original, delimiter=';')
                next(reader, None)
                for row in reader:
                    writer.writerow(row)
            os.remove(f'{DATA_DIR}/{arquivo}_SP.csv')

    dataset = pd.read_csv(f'{DATA_DIR}/candidato_deputados.csv',
                          header=0,
                          names=cols_cands,
                          encoding='latin-1',
                          sep=';')
    dataset = dataset[dataset['ds_cargo'] == 'DEPUTADO ESTADUAL']
    dataset.drop(columns=drop_cols_cands, inplace=True)
    save(dataset, 'cand')
    os.remove(f'{DATA_DIR}/candidato_deputados.csv')


def bens():
    url_base = 'http://agencia.tse.jus.br/estatistica/sead/odsele/bem_candidato/'
    arquivos = ['bem_candidato_2014', 'bem_candidato_2018']

    with open(f'{DATA_DIR}/candidato_bem.csv', 'a', newline='', encoding='latin-1') as infile:
        writer = csv.writer(infile, delimiter=';')

        for arquivo in arquivos:
            url = url_base + arquivo + '.zip'
            urlretrieve(url, f'{DATA_DIR}/{arquivo}.zip')
            with ZipFile(f'{DATA_DIR}/{arquivo}.zip', 'r') as zip_file:
                zip_file.extract(f'{arquivo}_SP.csv', path=f'{DATA_DIR}')
            os.remove(f'{DATA_DIR}/{arquivo}.zip')

            with open(f'{DATA_DIR}/{arquivo}_SP.csv', 'r', encoding='latin-1') as original:
                reader = csv.reader(original, delimiter=';')
                next(reader, None)
                for row in reader:
                    writer.writerow(row)
            os.remove(f'{DATA_DIR}/{arquivo}_SP.csv')

    bens = pd.read_csv(f'{DATA_DIR}/candidato_bem.csv',
                       header=0,
                       names=cols_bens,
                       encoding='latin-1',
                       sep=';',
                       decimal=',')
    cands = pd.read_csv(f'{DATA_DIR}/cand.csv')
    dataset = cands.merge(bens, on='sq_candidato', how='left')
    dataset['vlr_bem'].fillna(0.0, inplace=True)
    dataset.drop(columns=drop_cols_bens, inplace=True)
    dataset = dataset[[
        'dt_geracao_x', 'hh_geracao_x', 'ano_eleicao_x',
        'nm_tipo_eleicao_x', 'ds_eleicao_x', 'dt_eleicao_x',
        'sg_ue_x', 'nm_ue_x', 'sq_candidato', 'nr_candidato',
        'nm_candidato', 'nm_urna_candidato', 'nm_social_candidato',
        'nr_cpf_candidato', 'nr_ordem_candidato', 'ds_tp_bem',
        'ds_bem', 'vlr_bem']]
    dataset.columns = dataset.columns.str.replace('_x', '')

    save(dataset, 'cand_bens')
    os.remove(f'{DATA_DIR}/candidato_bem.csv')


def main():
    deps()
    bens()


if __name__ == '__main__':
    main()
