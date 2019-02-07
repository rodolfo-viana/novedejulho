import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/deputados/'
url_file = 'bases_eleitorais.xml'
url = url_base + url_file

def process_bases_eleitorais():
  xml_data = req.get(url).content
  dataset = xml_df(xml_data).process_data()
  dataset = dataset[['Id', 'Nome']]
  dataset = dataset.rename(columns={ 'Id': 'id', 'Nome': 'nm' })
  save_files(dataset, 'data', 'bases_eleitorais')

if __name__ == '__main__':
  process_bases_eleitorais()