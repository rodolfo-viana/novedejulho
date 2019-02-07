import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/deputados/'
url_file = 'partidos.xml'
url = url_base + url_file


def process_partidos():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['Numero', 'Sigla', 'Nome']]
    dataset = dataset.rename(columns={
        'Numero': 'nr', 'Sigla': 'sg', 'Nome': 'nm'
    })
    save_files(dataset, 'data', 'partidos')


if __name__ == '__main__':
    process_partidos()
