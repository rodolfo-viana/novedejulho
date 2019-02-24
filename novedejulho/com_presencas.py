import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/comissoes_permanentes_presencas.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'IdReuniao', 'IdPauta', 'IdDeputado', 'Deputado',
        'IdComissao', 'SiglaComissao', 'DataReuniao'
    ]]
    dataset = dataset.rename(columns={
        'IdReuniao': 'id_reuniao',
        'IdPauta': 'id_pauta',
        'IdDeputado': 'id_deputado',
        'Deputado': 'nm_deputado',
        'IdComissao': 'id_comissao',
        'SiglaComissao': 'sg_comissao',
        'DataReuniao': 'dt_comissao'
    })
    save_files(dataset, 'comissoes_presencas')


if __name__ == '__main__':
    main()
