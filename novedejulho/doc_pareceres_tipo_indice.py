import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/tipo_parecer.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['IdTipoParcer', 'TipoParecer']]
    dataset = dataset.rename(columns={
        'IdTipoParcer': 'id_tp_parecer',
        'TipoParecer': 'tp_parecer'
    })
    save_files(dataset, 'documentos_pareceres_tp_indice')


if __name__ == '__main__':
    main()
