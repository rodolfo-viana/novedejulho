import os
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

'''
Documentação:
al.sp.gov.br/repositorioDados/docs/processo_legislativo/propositura_parecer.pdf
'''

url_base = 'https://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
url_file = 'propositura_parecer.zip'
url = url_base + url_file


def fetch_data():
    urlretrieve(url, 'data/propositura_parecer.zip')
    zip_file = ZipFile('data/propositura_parecer.zip', 'r')
    zip_file.extractall('data')
    zip_file.close()
    os.remove('data/propositura_parecer.zip')


def process_proposicoes_pareceres():
    xml_data = 'data/propositura_parecer.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'AnoParecer', 'Descricao', 'Data', 'AdReferendum', 'RelatorEspecial',
        'VotoVencido', 'IdComissao', 'IdDocumento', 'IdParecer',
        'IdTipoParecer', 'TipoParecer', 'NrParecer', 'SiglaComissao',
        'TpParecer', 'URL'
    ]]
    dataset = dataset.rename(columns={
        'AnoParecer': 'ano', 'Descricao': 'ds_parecer', 'Data': 'dt_parecer',
        'AdReferendum': 'ad_referendum', 'RelatorEspecial': 'relator_especial',
        'VotoVencido': 'voto_vencido', 'IdComissao': 'id_comissao',
        'IdDocumento': 'id_documento', 'IdParecer': 'id_parecer',
        'IdTipoParecer': 'id_tp_parecer', 'TipoParecer': 'tp_parecer',
        'NrParecer': 'nr_parecer', 'SiglaComissao': 'sg_comissao',
        'TpParecer': 'cat_parecer', 'URL': 'url'
    })
    save_files(dataset, 'data', 'proposicoes_pareceres')
    os.remove(xml_data)


def main():
    fetch_data()
    process_proposicoes_pareceres()


if __name__ == '__main__':
    main()
