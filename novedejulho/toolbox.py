# Este código é inspirado no script 'helpers.py', usado em serenata-toolbox,
# componente da Operação Serenata de Amor. Conheça o projeto aqui:
# https://github.com/okfn-brasil/serenata-de-amor
# https://github.com/okfn-brasil/serenata-toolbox

import os
from datetime import datetime

XZ_PARAMS = {
    'compression': 'xz',
    'encoding': 'utf-8',
    'index': False
}

CSV_PARAMS = {
    'encoding': 'utf-8',
    'index': False
}


# Utilitários para extrair dados de xml

def xml_text(node, xpath):
    """
    :param node: o nó consultado
    :param xpath: o caminho ao texto do nó
    """
    text = node.find(xpath).text
    if text is not None:
        text = text.strip()
    return text


def xml_date(node, xpath, date_format='%d/%m/%Y'):
    """
    :param node: o nó consultado
    :param xpath: o caminho à data do nó
    """
    return datetime.strptime(xml_text(node, xpath), date_format)


def xml_datetime(node, xpath, datetime_format='%d/%m/%Y %H:%M:%S'):
    """
    :param node: o nó consultado
    :param xpath: o caminho à data/hora do nó
    """
    return datetime.strptime(xml_text(node, xpath), datetime_format)


# Utilitários para salvar os dados em csv comprimido e regular

def save_xz(df, data_dir, name):
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    file_path = os.path.join(data_dir, '{}-{}.xz'.format(today, name))
    df.to_csv(file_path, **XZ_PARAMS)


def save_csv(df, data_dir, name):
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    file_path = os.path.join(data_dir, '{}-{}.csv'.format(today, name))
    df.to_csv(file_path, **CSV_PARAMS)
