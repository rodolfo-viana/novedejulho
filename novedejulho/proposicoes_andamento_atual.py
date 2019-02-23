import os
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

from ndj_toolbox.fetch import (xml_df_internal, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/documento_andamento_atual.zip'
url = url_base + url_file


def main():
    hoje = datetime.strftime(datetime.now(), '%Y-%m-%d')
    DATA_DIR = f'data_{hoje}'
    file_path = os.path.join(DATA_DIR, 'documento_andamento_atual.zip')

    urlretrieve(url, file_path)
    zip_file = ZipFile(file_path, 'r')
    zip_file.extractall(DATA_DIR)
    zip_file.close()
    os.remove(file_path)

    xml_data = os.path.join(DATA_DIR, 'documento_andamento_atual.xml')
    dataset = xml_df_internal(xml_data).process_data()
    dataset = dataset[[
        'IdDocumento', 'Data', 'NrOrdem', 'Descricao',
        'IdTpAndamento', 'TpAndamento', 'IdEtapa',
        'NmEtapa', 'IdComissao', 'SiglaComissao'
    ]]
    dataset = dataset.rename(columns={
        'IdDocumento': 'id_documento', 'Data': 'dt',
        'NrOrdem': 'nr_ordem', 'Descricao': 'ds',
        'IdTpAndamento': 'id_tp_andamento', 'TpAndamento': 'tp_andamento',
        'IdEtapa': 'id_etapa', 'NmEtapa': 'nm_etapa',
        'IdComissao': 'id_comissao', 'SiglaComissao': 'sg_comissao'
    })

    dataset['ds'] = dataset['ds'].apply(remove_break_line)

    save_files(dataset, 'proposicoes_andamento_atual')
    os.remove(xml_data)


def remove_break_line(text):
    try:
        return text.replace('\n', '')
    except:
        return text


if __name__ == '__main__':
    main()
