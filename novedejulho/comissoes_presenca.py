import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

URL = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/comissoes_permanentes_presencas.xml'
arquivo = 'comissoes_presenca'
data_dir = 'data'

def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def process_request():
  xml_data = req.get(URL).content
  dataset = xml_df(xml_data).process_data()
  dataset = dataset[[
    'IdReuniao', 'IdPauta', 'IdDeputado',
    'Deputado', 'IdComissao', 'SiglaComissao',
    'DataReuniao'
  ]]
  dataset = dataset.rename(columns={
    'IdReuniao': 'id_reuniao',
    'IdPauta': 'id_pauta',
    'IdDeputado': 'id_deputado',
    'Deputado': 'nome_deputado',
    'IdComissao': 'id_comissao',
    'SiglaComissao': 'siga_comissao',
    'DataReuniao': 'data_comissao'
  })
  save_files(dataset, data_dir, arquivo)

if __name__ == '__main__':
  create_dir()
  process_request()