import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'legislacao/legislacao_temas.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['IdTema', 'Tema']]
    dataset = dataset.rename(columns={
        'IdTema': 'id_tema',
        'Tema': 'ds_tema'
    })
    save_files(dataset, 'legislacao_temas_indice')


if __name__ == '__main__':
    main()
