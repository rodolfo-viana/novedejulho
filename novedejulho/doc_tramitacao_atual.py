import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)
from ndj_toolbox.format import remove_break_line

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/documento_andamento_atual.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'

    urlretrieve(url, f'{DATA_DIR}/documento_andamento_atual.zip')
    zip_file = ZipFile(f'{DATA_DIR}/documento_andamento_atual.zip', 'r')
    zip_file.extractall(f'{DATA_DIR}')
    zip_file.close()
    os.remove(f'{DATA_DIR}/documento_andamento_atual.zip')

    xml_data = f'{DATA_DIR}/documento_andamento_atual.xml'
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'IdDocumento', 'Data', 'NrOrdem', 'Descricao',
        'IdTpAndamento', 'TpAndamento', 'IdEtapa',
        'NmEtapa', 'IdComissao', 'SiglaComissao'
    ]]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_documento',
        'Data': 'dt_tramitacao',
        'NrOrdem': 'nr_ordem',
        'Descricao': 'ds_andamento',
        'IdTpAndamento': 'id_tp_andamento',
        'TpAndamento': 'tp_andamento',
        'IdEtapa': 'id_etapa',
        'NmEtapa': 'nm_etapa',
        'IdComissao': 'id_comissao',
        'SiglaComissao': 'sg_comissao'
    })

    dataset['ds_andamento'] = dataset['ds_andamento'].apply(remove_break_line)

    save_files(dataset, 'documentos_tramitacao')
    os.remove(xml_data)


if __name__ == '__main__':
    main()
