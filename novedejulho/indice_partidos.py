import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'deputados/partidos.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['Numero', 'Sigla', 'Nome']]
    dataset = dataset.rename(columns={
        'Numero': 'nr_partido', 'Sigla': 'sg_partido', 'Nome': 'nm_partido'
    })
    save_files(dataset, 'indice_partidos')


if __name__ == '__main__':
    main()
