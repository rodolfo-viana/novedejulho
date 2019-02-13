import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/comissoes.xml'
url = url_base + url_file


def process_comissoes():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'IdComissao', 'NomeComissao', 'SiglaComissao',
        'DescricaoComissao', 'DataFimComissao'
    ]]
    dataset = dataset.rename(columns={
        'IdComissao': 'id_comissao', 'NomeComissao': 'nm_comissao',
        'SiglaComissao': 'sg_comissao', 'DescricaoComissao': 'ds_comissao',
        'DataFimComissao': 'dt_fim_comissao',
    })
    save_files(dataset, 'data', 'indice_comissoes')


def main():
    process_comissoes()


if __name__ == '__main__':
    main()
