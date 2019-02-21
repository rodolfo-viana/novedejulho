import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'deputados/deputado_base_eleitoral.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['IdDeputado', 'IdBaseEleitoral', 'NrOrdem']]
    dataset = dataset.rename(columns={
        'IdDeputado': 'id_deputado', 'IdBaseEleitoral': 'id_base',
        'NrOrdem': 'nr_ordem'
    })
    save_files(dataset, 'deputados_base_eleitoral')


if __name__ == '__main__':
    main()
