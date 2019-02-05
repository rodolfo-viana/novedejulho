import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/naturezasSpl.xml'
url = url_base + url_file


def process_proposicoes_natureza():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['idNatureza', 'nmNatureza', 'sgNatureza', 'tpNatureza']]
    dataset = dataset.rename(columns={
        'idNatureza': 'id_natureza', 'nmNatureza': 'nm_natureza',
        'sgNatureza': 'sg_natureza', 'tpNatureza': 'tp_natureza'
    })
    save_files(dataset, 'data', 'proposicoes_natureza')


if __name__ == '__main__':
    process_proposicoes_natureza()
