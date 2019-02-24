import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/propositura_parecer.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    urlretrieve(url, f'{DATA_DIR}/propositura_parecer.zip')
    zip_file = ZipFile(f'{DATA_DIR}/propositura_parecer.zip', 'r')
    zip_file.extractall(f'{DATA_DIR}')
    zip_file.close()
    os.remove(f'{DATA_DIR}/propositura_parecer.zip')

    xml_data = f'{DATA_DIR}/propositura_parecer.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'AnoParecer', 'Descricao', 'Data', 'AdReferendum', 'RelatorEspecial',
        'VotoVencido', 'IdComissao', 'IdDocumento', 'IdParecer',
        'IdTipoParecer', 'TipoParecer', 'NrParecer', 'SiglaComissao',
        'TpParecer', 'URL'
    ]]
    dataset = dataset.rename(columns={
        'AnoParecer': 'tx_ano_parecer',
        'Data': 'dt_parecer',
        'IdComissao': 'id_comissao',
        'SiglaComissao': 'sg_comissao',
        'IdDocumento': 'id_documento',
        'IdParecer': 'id_parecer',
        'IdTipoParecer': 'id_tp_parecer',
        'TipoParecer': 'tp_parecer',
        'NrParecer': 'nr_parecer',
        'TpParecer': 'cat_parecer',
        'Descricao': 'ds_parecer',
        'AdReferendum': 'tx_adreferendum',
        'RelatorEspecial': 'tx_relator_especial',
        'VotoVencido': 'tx_voto_vencido',
        'URL': 'tx_url'
    })
    save_files(dataset, 'documentos_pareceres')
    os.remove(xml_data)


if __name__ == '__main__':
    main()
