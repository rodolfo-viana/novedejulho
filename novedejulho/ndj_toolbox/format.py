import os
import glob
import csv
import sqlite3
from datetime import datetime
import pandas as pd


# Utilitário para junção de dataframes em 'cand_bens.py'

def merge_dfs():
    cands = pd.read_csv(f'{DATA_DIR}/candidatos.csv')
    dataset = cands.merge(bens, on='sq_candidato', how='left')
    dataset['vlr_bem'].fillna(0, inplace=True)
    sanitize_float(dataset['vlr_bem'], inplace=True)
    dataset.drop(columns=[
        'dt_geracao_x', 'hh_geracao_x', 'ano_eleicao_x', 'cd_tipo_eleicao_x',
        'nm_tipo_eleicao_x', 'nr_turno', 'cd_eleicao_x', 'ds_eleicao_x',
        'dt_eleicao_x', 'tp_abrangencia', 'sg_uf_x', 'sg_ue_x', 'nm_ue_x',
        'cd_cargo', 'ds_cargo', 'nm_email', 'cd_situacao_candidatura', 'ds_situacao_candidatura',
        'cd_detalhe_situacao_cand', 'ds_detalhe_situacao_cand', 'tp_agremiacao',
        'nr_partido', 'sg_partido', 'nm_partido', 'sq_coligacao',
        'nm_coligacao', 'ds_composicao_coligacao', 'cd_nacionalidade',
        'ds_nacionalidade', 'sg_uf_nascimento', 'cd_municipio_nascimento',
        'nm_municipio_nascimento', 'dt_nascimento', 'nr_idade_data_posse',
        'nr_titulo_eleitoral_candidato', 'cd_genero', 'ds_genero',
        'cd_grau_instrucao', 'ds_grau_instrucao', 'cd_estado_civil',
        'ds_estado_civil', 'cd_cor_raca', 'ds_cor_raca', 'cd_ocupacao',
        'ds_ocupacao', 'nr_despesa_max_campanha', 'cd_sit_tot_turno',
        'ds_sit_tot_turno', 'st_reeleicao', 'st_declarar_bens',
        'nr_protocolo_candidatura', 'nr_processo'
    ], inplace=True)
    dataset = dataset[[
        'dt_geracao_y', 'hh_geracao_y', 'ano_eleicao_y', 'cd_tipo_eleicao_y',
        'nm_tipo_eleicao_y', 'cd_eleicao_y', 'ds_eleicao_y', 'dt_eleicao_y',
        'sg_uf_y', 'sg_ue_y', 'nm_ue_y', 'sq_candidato', 'nr_candidato', 'nm_candidato',
        'nm_urna_candidato', 'nm_social_candidato', 'nr_cpf_candidato', 'nr_ordem_candidato',
        'cd_tp_bem', 'ds_tp_bem', 'ds_bem', 'vlr_bem', 'dt_ultima_atualizacao',
        'hh_ultima_atualizacao']]
    dataset.columns = dataset.columns.str.replace('_y', '')


# Utilitário para remover newline

def remove_break_line(text):
    try:
        return text.replace('\n', '')
    except:
        return text


# Utilitário para transformar em float e converter vírgula em ponto

def sanitize_float(item):
    return float(item.get_text().strip().replace('.', '').replace(',', '.'))


# Utilitário para limpar a coluna 'tp_categoria' - ref.: deputados_gastos_cota.py

def clean_expenses_categories(df):
    df['tp_categoria'].replace({
        'A - COMBUSTÍVEIS E LUBRIFICANTES': 'COMBUSTÍVEIS E LUBRIFICANTES',
        'B - LOCAÇÃO E MANUT DE BENS MÓVEIS E IMÓVEIS, CONDOMÍNIOS E OUTROS': 'LOCAÇÃO E MANUTENÇÃO DE BENS MÓVEIS, IMÓVEIS E CONDOMÍNIO',
        'C - MATERIAIS E SERVIÇOS DE MANUT E CONSERV DE VEÍCULOS ; PEDÁGIOS': 'MANUTENÇÃO DE VEÍCULOS E PEDÁGIOS',
        'D - MATERIAIS E SERVIÇOS GRÁFICOS, DE CÓPIAS  E REPRODUÇÃO DE DOCS': 'SERVIÇOS GRÁFICOS',
        'E - MATERIAIS DE ESCRITÓRIO E OUTROS MATERIAIS DE CONSUMO': 'MATERIAL DE ESCRITÓRIO',
        'F - SERVIÇOS TÉCNICOS PROFISSIONAIS (CONSULTORIA, PESQUISAS ETC)': 'SERVIÇOS TÉCNICOS E CONSULTORIAS',
        'G - ASSINATURAS DE PERIÓDICOS, PUBLICAÇÕES E INTERNET': 'ASSINATURA DE JORNAIS, REVISTAS E INTERNET',
        'H - SERV.UTIL.PÚBLICA (TELEF.MÓVEL/FIXA, ENERGIA, ÁGUA, GÁS ETC)': 'TELEFONE, ENERGIA, ÁGUA E OUTROS SERVIÇOS',
        'I - HOSPEDAGEM, ALIMENTAÇÃO E DESPESAS DE LOCOMOÇÃO': 'ALIMENTAÇÃO, HOSPEDAGEM E LOCOMOÇÃO',
        'J - SERVIÇOS DE COMUNICAÇÃO': 'SERVIÇOS DE COMUNICAÇÃO',
        'K - LOCAÇÃO DE BENS MÓVEIS': 'LOCAÇÃO DE BENS MÓVEIS',
        'L - LOCAÇÃO DE BENS IMÓVEIS': 'LOCAÇÃO DE IMÓVEIS',
        'M - MANUTENÇÃO DE BENS MÓVEIS,  IMÓVEIS, CONDOMÍNIOS E OUTROS': 'MANUTENÇÃO DE BENS MÓVEIS, IMÓVEIS E CONDOMÍNIO',
        'N - MORADIA': 'MORADIA'}, inplace=True)


# Utiliários para criar e popular database

def generate_db():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'
    for csvFile in glob.glob(f'{DATA_DIR}/*.csv'):
        file_name = os.path.basename(csvFile)
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
