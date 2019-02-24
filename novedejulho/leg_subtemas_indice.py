import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'legislacao/legislacao_subtemas.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['IdSubTema', 'SubTema']]
    dataset = dataset.rename(columns={
        'IdSubTema': 'id_subtema',
        'SubTema': 'ds_subtema'
    })
    save_files(dataset, 'legislacao_subtemas_indice')


if __name__ == '__main__':
    main()
