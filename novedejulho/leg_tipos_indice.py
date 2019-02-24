import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'legislacao/legislacao_tipo_normas.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['IdTipo', 'DsTipo']]
    dataset = dataset.rename(columns={
        'IdTipo': 'id_tp_norma',
        'DsTipo': 'ds_tp_norma'
    })
    save_files(dataset, 'legislacao_tipos_indice')


if __name__ == '__main__':
    main()
