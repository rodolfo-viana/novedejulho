import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/deputados/'
url_file = 'areas_atuacao.xml'
url = url_base + url_file


def process_areas_atuacao():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['Id', 'Nome']]
    dataset = dataset.rename(columns={'Id': 'id_area', 'Nome': 'nm_area'})
    save_files(dataset, 'data', 'indice_areas_atuacao')


def main():
    process_areas_atuacao()


if __name__ == '__main__':
    main()
