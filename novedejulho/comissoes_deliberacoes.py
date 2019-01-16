import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url = 'https://www.al.sp.gov.br/repositorioDados/processo_legislativo/comissoes_permanentes_deliberacoes.xml'
arquivo = 'comissoes_deliberacoes'
data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def process_request():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['IdReuniao', 'IdDocumento', 'IdPauta', 'NrOrdem',
                       'DataInclusao', 'DataSaida', 'Deliberacao',
                       'IdDeliberacao']]
    dataset = dataset.rename(columns={
        'IdReuniao': 'id_reuniao', 'IdDocumento': 'id_documento',
        'IdPauta': 'id_pauta', 'NrOrdem': 'nr_ordem',
        'DataInclusao': 'dt_inclusao', 'DataSaida': 'dt_saida',
        'Deliberacao': 'deliberacao', 'IdDeliberacao': 'id_deliberacao'
    })
    save_files(dataset, data_dir, arquivo)


if __name__ == '__main__':
    create_dir()
    process_request()
