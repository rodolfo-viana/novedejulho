import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

URL = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/comissoes_permanentes_votacoes.xml'
arquivo = 'comissoes_votacoes'
data_dir = 'data'

def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def process_request():
  xml_data = req.get(URL).content
  dataset = xml_df(xml_data).process_data()
  dataset = dataset[[
    'IdReuniao', 'IdPauta', 'IdComissao',
    'IdDocumento', 'IdDeputado', 'Deputado',
    'TipoVoto', 'Voto'
  ]]
  dataset = dataset.rename(columns={
    'IdReuniao': 'id_reuniao',
    'IdPauta': 'id_pauta',
    'IdComissao': 'id_comissao',
    'IdDocumento': 'id_documento',
    'IdDeputado': 'id_deputado',
    'Deputado': 'nome_deputado',
    'TipoVoto': 'tipo_voto',
    'Voto': 'voto'
  })
  save_files(dataset, data_dir, arquivo)

if __name__ == '__main__':
  create_dir()
  process_request()