import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/comissoes_permanentes_deliberacoes.xml'
url = url_base + url_file


def process_comissoes_deliberacoes():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'IdReuniao', 'IdDocumento', 'IdPauta', 'NrOrdem', 'DataInclusao',
        'DataSaida', 'Deliberacao', 'IdDeliberacao'
    ]]
    dataset = dataset.rename(columns={
        'IdReuniao': 'id_reuniao', 'IdDocumento': 'id_documento',
        'IdPauta': 'id_pauta', 'NrOrdem': 'nr_ordem',
        'DataInclusao': 'dt_inclusao', 'DataSaida': 'dt_saida',
        'Deliberacao': 'deliberacao', 'IdDeliberacao': 'id_deliberacao'
    })
    save_files(dataset, 'data', 'comissoes_deliberacoes')


def main():
    process_comissoes_deliberacoes()


if __name__ == '__main__':
    main()
