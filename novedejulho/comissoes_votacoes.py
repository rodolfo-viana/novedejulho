import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/comissoes_permanentes_votacoes.xml'
url = url_base + url_file


def process_comissoes_votacoes():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'IdReuniao', 'IdPauta', 'IdComissao', 'IdDocumento',
        'IdDeputado', 'Deputado', 'TipoVoto', 'Voto'
    ]]
    dataset = dataset.rename(columns={
        'IdReuniao': 'id_reuniao', 'IdPauta': 'id_pauta',
        'IdComissao': 'id_comissao', 'IdDocumento': 'id_documento',
        'IdDeputado': 'id_deputado', 'Deputado': 'nm_deputado',
        'TipoVoto': 'tp_voto', 'Voto': 'voto'
    })
    save_files(dataset, 'data', 'comissoes_votacoes')


def main():
    process_comissoes_votacoes()


if __name__ == '__main__':
    main()
